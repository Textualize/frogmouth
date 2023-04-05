"""Provides the local files navigation pane."""

from os import getenv
from pathlib import Path

from httpx import URL


from textual.app import ComposeResult
from textual.message import Message
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

    class Goto(Message):
        """Message that requests the viewer goes to a given location."""

        def __init__(self, location: Path | URL) -> None:
            """Initialise the history goto message.

            Args:
                location: The location to go to.
            """
            super().__init__()
            self.location = location
            """The location to go to."""

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle a file being selected in the directory tree.

        Args:
            event: The direct tree selection event.
        """
        event.stop()
        self.post_message(self.Goto(Path(event.path)))
