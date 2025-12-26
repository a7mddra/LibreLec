import time
import os
from .config import Config

class SlideScraper:
    def __init__(self, page):
        self.page = page

    def find_target_frame(self):
        """
        Intelligently hunts for the DRM-protected viewer URL inside iframes.
        """
        # Wait a moment for iframes to populate
        time.sleep(2)
        
        # 1. Check current URL
        for k in Config.VIEWER_KEYWORDS:
            if k in self.page.url:
                return self.page.url

        # 2. Check Iframes
        for frame in self.page.frames:
            try:
                src = frame.url
                for k in Config.VIEWER_KEYWORDS:
                    if k in src:
                        return src
            except:
                continue
                
        return None

    def get_slide_elements(self):
        """Finds all page elements in the DOM."""
        return self.page.locator(Config.SELECTOR_PAGE).all()

    def extract_slides(self, temp_dir, progress_callback=None):
        """
        Generator that yields progress for each extracted slide.
        """
        page_elements = self.get_slide_elements()
        total_pages = len(page_elements)
        
        if total_pages == 0:
            # Retry once
            time.sleep(3)
            page_elements = self.get_slide_elements()
            total_pages = len(page_elements)

        if total_pages == 0:
            return 0 

        for index, page_handle in enumerate(page_elements):
            page_num = index + 1
            
            # Scroll
            page_handle.scroll_into_view_if_needed()
            
            try:
                # Wait for canvas render
                canvas = page_handle.locator(Config.SELECTOR_CANVAS)
                canvas.wait_for(state="visible", timeout=Config.TIMEOUT_CANVAS)
                time.sleep(0.3) # Stabilization
                
                # Capture
                output_path = os.path.join(temp_dir, f"slide_{page_num:03d}.png")
                canvas.screenshot(path=output_path)
                
            except Exception:
                # Fallback
                fallback_path = os.path.join(temp_dir, f"slide_{page_num:03d}_fallback.png")
                page_handle.screenshot(path=fallback_path)

            if progress_callback:
                progress_callback(1)
                
        return total_pages
