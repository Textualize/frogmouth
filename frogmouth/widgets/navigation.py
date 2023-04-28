"""Provides the navigation panel widget."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import var
from textual.widgets import TabbedContent, Tabs
from typing_extensions import Self

from .navigation_panes.bookmarks import Bookmarks
from .navigation_panes.history import History
from .navigation_panes.local_files import LocalFiles
from .navigation_panes.table_of_contents import TableOfContents


class Navigation(Vertical, can_focus=False, can_focus_children=True):
    """A navigation panel widget."""

    DEFAULT_CSS = """
    Navigation {
        width: 44;
        background: $panel;
        display: block;
        dock: left;
    }

    Navigation.hidden {
        display: none;
    }

    TabbedContent {
        height: 100% !important;
    }

    ContentSwitcher {
        height: 1fr !important;
    }
    """

    BINDINGS = [
        Binding("comma,a,ctrl+left,shift+left,h", "previous_tab", "", show=False),
        Binding("full_stop,d,ctrl+right,shift+right,l", "next_tab", "", show=False),
    ]
    """Bindings local to the navigation pane."""

    popped_out: var[bool] = var(False)
    """Is the navigation popped out?"""

    def compose(self) -> ComposeResult:
        """Compose the content of the navigation pane."""
        self.popped_out = False
        # pylint:disable=attribute-defined-outside-init
        self._contents = TableOfContents()
        self._local_files = LocalFiles()
        self._bookmarks = Bookmarks()
        self._history = History()
        with TabbedContent() as tabs:
            self._tabs = tabs
            yield self._contents
            yield self._local_files
            yield self._bookmarks
            yield self._history

    def watch_popped_out(self) -> None:
        """Watch for changes to the popped out state."""
        self.set_class(not self.popped_out, "hidden")

    def toggle(self) -> None:
        """Toggle the popped/unpopped state."""
        self.popped_out = not self.popped_out

    @property
    def table_of_contents(self) -> TableOfContents:
        """The table of contents widget."""
        return self._contents

    @property
    def local_files(self) -> LocalFiles:
        """The local files widget."""
        return self._local_files

    @property
    def bookmarks(self) -> Bookmarks:
        """The bookmarks widget."""
        return self._bookmarks

    @property
    def history(self) -> History:
        """The history widget."""
        return self._history

    async def jump_to_local_files(self, target: Path | None = None) -> Self:
        """Switch to and focus the local files pane.

        Returns:
            Self.
        """
        self.popped_out = True
        if target is not None:
            await self._local_files.chdir(target)
        self._local_files.activate()
        self.focus_tab()
        return self

    def jump_to_bookmarks(self) -> Self:
        """Switch to and focus the bookmarks pane.

        Returns:
            Self.
        """
        self.popped_out = True
        self._bookmarks.activate()
        self.focus_tab()
        return self

    def jump_to_history(self) -> Self:
        """Switch to and focus the history pane.

        Returns:
            Self.
        """
        self.popped_out = True
        self._history.activate()
        self.focus_tab()
        return self

    def jump_to_contents(self) -> Self:
        """Switch to and focus the table of contents pane.

        Returns:
            Self.
        """
        self.popped_out = True
        self._contents.activate()
        self.focus_tab()
        return self

    def action_previous_tab(self) -> None:
        """Switch to the previous tab in the navigation pane."""
        self.query_one(Tabs).action_previous_tab()
        self.focus_tab()

    def action_next_tab(self) -> None:
        """Switch to the next tab in the navigation pane."""
        self.query_one(Tabs).action_next_tab()
        self.focus_tab()

    def focus_tab(self) -> None:
        """Focus the currently active tab."""
        active = self.query_one(Tabs).active
        if active == "contents":
            self._contents.query_one("MarkdownTableOfContents > Tree").focus(
                scroll_visible=False
            )
        elif active == "local":
            self._local_files.query_one("DirectoryTree").focus(scroll_visible=False)
        elif active == "bookmarks":
            self._bookmarks.query_one("OptionList").focus(scroll_visible=False)
        elif active == "history":
            self._history.query_one("OptionList").focus(scroll_visible=False)
