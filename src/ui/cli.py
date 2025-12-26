import sys
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

class CLI:
    def __init__(self):
        self.console = Console()

    def show_welcome(self):
        self.console.clear()
        self.console.print(Text(" unlk-lec v1.0 ", style="bold magenta"))

    def get_initial_choice(self):
        return questionary.select(
            "What type of lecture do you want to extract?",
            choices=[
                "PDF Document",
                questionary.Choice("Video Stream (Soon)", disabled="Not implemented yet"),
                "Exit"
            ],
            pointer=">"
        ).ask()

    def get_url(self):
        return questionary.text("Paste the University Login URL (.edu):").ask()

    def show_launching_message(self):
        self.console.print("[dim]Launching Chromium Hook...[/dim]")

    def show_manual_login_instructions(self):
        self.console.print("\n[bold yellow]⚠ ACTION REQUIRED:[/]")
        self.console.print("1. Log in manually in the browser window.")
        self.console.print("2. Navigate to the page containing the Locked PDF.")
        self.console.print("\n[bold cyan]--- READY FOR EXTRACTION ---[/]")

    def wait_for_enter(self):
        input("Press [ENTER] when the PDF page is open on screen...")

    def show_drm_found(self, src):
        self.console.print(f"[green]✔ DRM Source Found:[/green] [dim]{src}[/dim]")

    def show_isolation_message(self):
        self.console.print("[italic]Isolating viewer...[/]")

    def ask_confirm_extraction(self):
        # Fallback to input() to avoid async conflicts inside loop
        res = input("Try extraction anyway on current view? [y/N]: ").strip().lower()
        return res == 'y'

    def get_pdf_name(self, default_name=""):
        # Fallback to input() to avoid async conflicts inside loop
        prompt = f"Enter Output Filename [{default_name}]: " if default_name else "Enter Output Filename: "
        return input(prompt).strip()

    def show_extraction_start(self, pdf_name):
        self.console.clear()
        self.console.print(Panel(Text(" INITIATING CANVAS HIJACK PROTOCOL ", style="bold green on black"), border_style="green"))

    def create_progress_context(self):
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        )

    def show_error(self, message):
        self.console.print(f"[bold red]❌ ERROR: {message}[/]")

    def show_success(self, path):
        self.console.print(f"\n[bold green]SUCCESS[/] 🔓 \nArtifact saved to: [underline]{path}[/]")

    def ask_next_step(self):
        # Fallback to input() to avoid async conflicts inside loop
        print("\nOperation Complete.")
        res = input("Extract Another PDF? [Y/n]: ").strip().lower()
        if res == 'n':
            return "Quit"
        return "Extract Another PDF"
