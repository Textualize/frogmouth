"""Provides the local files navigation pane."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import os

from httpx import URL
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import DirectoryTree
from textual.types import DirEntry

from ...utility import maybe_markdown
from .navigation_pane import NavigationPane


class FilteredDirectoryTree(DirectoryTree):  # pylint:disable=too-many-ancestors
    """A `DirectoryTree` filtered for the markdown viewer."""

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        """Filter the directory tree for the Markdown viewer.

        Args:
            paths: The paths to be filtered.

        Returns:
            The parts filtered for the Markdown viewer.

        The filtered set will include all filesystem entries that aren't
        hidden (in a Unix sense of hidden) which are either a directory or a
        file that looks like it could be a Markdown document.
        """
        try:
            return [
                path
                for path in paths
                if not path.name.startswith(".")
                and path.is_dir()
                or (path.is_file() and maybe_markdown(path))
            ]
        except PermissionError:
            return []


class LocalFiles(NavigationPane):
    """Local file picking navigation pane."""

    DEFAULT_CSS = """
    LocalFiles {
        height: 100%;
    }

    LocalFiles > DirectoryTree {
        background: $panel;
        width: 1fr;
    }

    LocalFiles > DirectoryTree:focus .tree--cursor, LocalFiles > DirectoryTree .tree--cursor {
        background: $accent 50%;
        color: $text;
    }
    """

    def __init__(self) -> None:
        """Initialise the local files navigation pane."""
        super().__init__("Local")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield FilteredDirectoryTree(Path("~").expanduser())

    def chdir(self, path: Path) -> None:
        """Change the filesystem view to the given directory.

        Args:
            path: The path to change to.
        """
        self.query_one(FilteredDirectoryTree).path = path

    def set_focus_within(self) -> None:
        """Focus the directory tree.."""
        self.query_one(DirectoryTree).focus(scroll_visible=False)

    class Goto(Message):
        """Message that requests the viewer goes to a given location."""

        def __init__(self, location: Path | URL, focus_viewer:bool) -> None:
            """Initialise the history goto message.

            Args:
                location: The location to go to.
            """
            super().__init__()
            self.location = location
            """The location to go to."""
            self.focus_viewer = focus_viewer
            """Viewer has to be focused or not"""

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle a file being selected in the directory tree.

        Args:
            event: The direct tree selection event.
        """
        event.stop()
        self.post_message(self.Goto(Path(event.path) , True))
   
    def on_tree_node_highlighted(self, event: DirectoryTree.NodeHighlighted):
        """Handle node highlight in directory tree.

        Args:
            event: The directory node highlight event.
        """
        
        event.stop()
        if not event.node.data:
            return
        pathEntry: DirEntry = event.node.data

        return os.path.isfile(pathEntry.path) and self.post_message(self.Goto(Path(pathEntry.path), False))