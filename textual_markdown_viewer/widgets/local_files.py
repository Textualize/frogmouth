"""Provides the local files navigation pane."""

from os import getenv


from textual.app import ComposeResult
from textual.widgets import DirectoryTree, TabPane


class LocalFiles(TabPane):
    """Local file picking navigation pane."""

    DEFAULT_CSS = """
    LocalFiles {
        height: 100%;
    }

    LocalFiles > DirectoryTree {
        background: $primary;
        width: 1fr;
    }
    """

    def __init__(self) -> None:
        """Initialise the local files navigation pane."""
        super().__init__("Local")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield DirectoryTree(getenv("HOME") or ".")
