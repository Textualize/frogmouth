"""Provides the navigation panel widget."""

from os import getenv
from pathlib import Path
from typing_extensions import Self

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
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
        yield DirectoryTree(getenv("HOME") or ".")


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
        # pylint:disable=attribute-defined-outside-init
        with TabbedContent() as tabs:
            self._tabs = tabs
            self._local_files = LocalFiles()
            self._bookmarks = Bookmarks()
            yield self._local_files
            yield self._bookmarks

    class VisitLocalFile(Message):
        """Message sent when the user wants to visit a local file."""

        def __init__(self, visit: Path) -> None:
            """Initialise the mesage.

            Args:
                visit: The path to the file to visit.
            """
            super().__init__()
            self.visit = visit

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle a file being selected in the directory tree.

        Args:
            event: The direct tree selection event.
        """
        event.stop()
        self.post_message(self.VisitLocalFile(Path(event.path)))

    def jump_to_local_files(self) -> Self:
        """Switch to and focus the local files pane.

        Returns:
            Self.
        """
        if self._local_files.id is not None:
            self._tabs.active = self._local_files.id
            self._local_files.children[0].focus()
        return self

    def jump_to_bookmarks(self) -> Self:
        """Switch to and focus the bookmarks pane.

        Returns:
            Self.
        """
        if self._bookmarks.id is not None:
            self._tabs.active = self._bookmarks.id
            # TODO: Focus the content when I add it.
        return self
