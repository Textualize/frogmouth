"""Provides the navigation panel widget."""

from pathlib import Path
from typing_extensions import Self

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import DirectoryTree, TabbedContent


from .bookmarks import Bookmarks
from .history import History
from .local_files import LocalFiles


class Navigation(Vertical):
    """A navigation panel widget."""

    DEFAULT_CSS = """
    Navigation {
        width: 1fr;
        background: $primary;
        display: none;
    }

    Navigation:focus-within {
        display: block;
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
            self._history = History()
            yield self._local_files
            yield self._bookmarks
            yield self._history

    @property
    def history(self) -> History:
        """The history widget."""
        return self._history

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

    def jump_to_history(self) -> Self:
        """Switch to and focus the history pane.

        Returns:
            Self.
        """
        if self._history.id is not None:
            self._tabs.active = self._history.id
            self._history.children[0].focus()
        return self
