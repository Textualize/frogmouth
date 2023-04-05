"""Provides the navigation panel widget."""

from typing_extensions import Self

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import TabbedContent, Tabs


from .bookmarks import Bookmarks
from .history import History
from .local_files import LocalFiles
from .table_of_contents import TableOfContents


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

    BINDINGS = [
        Binding("left", "previous_tab", "", show=False),
        Binding("right", "next_tab", "", show=False),
    ]
    """Bindings local to the navigation pane."""

    def compose(self) -> ComposeResult:
        """Compose the content of the navigation pane."""
        # pylint:disable=attribute-defined-outside-init
        with TabbedContent() as tabs:
            self._tabs = tabs
            self._contents = TableOfContents()
            self._local_files = LocalFiles()
            self._bookmarks = Bookmarks()
            self._history = History()
            yield self._contents
            yield self._local_files
            yield self._bookmarks
            yield self._history

    @property
    def history(self) -> History:
        """The history widget."""
        return self._history

    @property
    def table_of_contents(self) -> TableOfContents:
        """The table of contents widget."""
        return self._contents

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

    def jump_to_contents(self) -> Self:
        """Switch to and focus the table of contents pane.

        Returns:
            Self.
        """
        if self._contents.id is not None:
            self._tabs.active = self._contents.id
            self._contents.children[0].children[0].focus()
        return self

    def action_previous_tab(self) -> None:
        """Switch to the previous tab in the navigation pane."""
        self.query_one(Tabs).action_previous_tab()

    def action_next_tab(self) -> None:
        """Switch to the next tab in the navigation pane."""
        self.query_one(Tabs).action_next_tab()
