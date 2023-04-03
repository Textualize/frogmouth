"""Provides the navigation panel widget."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import DirectoryTree, TabbedContent, TabPane


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
        yield DirectoryTree(".")


class Bookmarks(TabPane):
    """Bookmarks navigation pane."""

    def __init__(self) -> None:
        """Initialise the bookmarks navigation pane."""
        super().__init__("Bookmarks")


class Navigation(Vertical):
    """A navigation panel widget."""

    DEFAULT_CSS = """
    Navigation {
        width: 1fr;
        background: $primary;
    }

    TabbedContent {
        height: 100% !important;
    }

    ContentSwitcher {
        height: 1fr !important;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the content of the navigation pane."""
        with TabbedContent():
            yield LocalFiles()
            yield Bookmarks()
