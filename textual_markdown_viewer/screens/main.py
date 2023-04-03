"""The main screen for the application."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header


class Main(Screen):
    """The main screen for the application."""

    def compose(self) -> ComposeResult:
        """Compose the main screen.."""
        yield Header()
        yield Footer()
