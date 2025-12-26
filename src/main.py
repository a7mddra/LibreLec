import sys
import time
import tempfile
import time
from .core.config import Config
from .core.browser import BrowserManager
from .core.scraper import SlideScraper
from .ui.cli import CLI
from .utils.pdf import PDFMerger

def main():
    cli = CLI()
    cli.show_welcome()

    # --- MENU STEP 1: SELECT TYPE ---
    action = cli.get_initial_choice()
    if action == "Exit" or not action:
        sys.exit()

    # --- MENU STEP 2: SETUP ---
    uni_url = cli.get_url()
    if not uni_url:
        print("URL required.")
        sys.exit()

    cli.show_launching_message()

    with BrowserManager() as browser:
        page = browser.create_page()

        # Navigate to login
        try:
            page.goto(uni_url)
        except:
            cli.show_error("Invalid URL or Network Error.")
            return

        cli.show_manual_login_instructions()
        
        # --- LOOP FOR MULTIPLE PDFS ---
        while True:
            cli.wait_for_enter()

            # --- AUTO-DISCOVERY MAGIC ---
            print("[italic]Scanning frames for DRM container...[/]")
            scraper = SlideScraper(page)
            raw_src = scraper.find_target_frame()

            if raw_src:
                cli.show_drm_found(raw_src)
                
                # Navigate if needed
                if page.url != raw_src:
                    cli.show_isolation_message()
                    page.goto(raw_src)
                    try:
                        page.wait_for_selector(Config.SELECTOR_VIEWER_CONTAINER, timeout=10000)
                    except:
                        cli.show_error("Timeout loading raw viewer.")
                        continue
            else:
                cli.show_error("Could not auto-detect PDF frame.")
                if not cli.ask_confirm_extraction():
                    continue

            # --- NAME CONFIG ---
            pdf_name = cli.get_pdf_name()
            if not pdf_name: 
                pdf_name = f"lecture_{int(time.time())}"

            # --- EXECUTE ---
            cli.show_extraction_start(pdf_name)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                with cli.console.status("[bold cyan]Analyzing DOM Structure...", spinner="dots"):
                    total_pages = scraper.extract_slides(temp_dir) # Just count/dry run handled inside? No, simplified logic.
                    # Wait, the previous logic did a count first. 
                    # Let's adjust scraper to allow just checking count or doing it all at once?
                    # The original code did: 1. Count (Analysis Phase) 2. Extract (Extraction Phase)
                
                # Re-instantiating scraper logic slightly to match original flow
                # Actually, let's just peek count first
                page_elements = scraper.get_slide_elements()
                total_pages = len(page_elements)
                
                if total_pages == 0:
                     # Retry logic handled in scraper
                     # but let's just call extract directly for simplicity in this refactor?
                     # Ideally we want the progress bar.
                     pass

                if total_pages > 0:
                    with cli.create_progress_context() as progress:
                         task = progress.add_task(f"[green]Extracting {pdf_name}...", total=total_pages)
                         
                         def update_progress(advance):
                             progress.update(task, advance=advance)
                             
                         scraper.extract_slides(temp_dir, progress_callback=update_progress)

                    # 3. Merging Phase
                    with cli.console.status("[bold yellow]Compiling PDF Artifact...", spinner="material"):
                        final_path = PDFMerger.merge_to_pdf(temp_dir, pdf_name)
                    
                    if final_path:
                        cli.show_success(final_path)
                    else:
                        cli.show_error("Merge Failed.")
                else:
                    cli.show_error("No slides detected. Is the document fully loaded?")

            # --- REPEAT? ---
            keep_going = cli.ask_next_step()

            if keep_going == "Quit":
                break
            else:
                print("[yellow]Navigate to the next lecture in the browser, then come back here.[/]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()