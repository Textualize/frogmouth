"""The main application class for the Markdown viewer."""

from textual.app import App

from .. import __version__
from ..screens import Main


class MarkdownViewer(App[None]):
    """The main application class."""

    TITLE = "Textual Markdown Viewer"
    """The main title for the application."""

    SUB_TITLE = f"{__version__}"
    """The sub-title for the application."""

    def on_mount(self) -> None:
        """Set up the application after the DOM is ready."""
        self.push_screen(Main())
