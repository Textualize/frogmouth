"""Provides the bookmarks navigation pane."""

from __future__ import annotations

from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import OptionList
from textual.widgets.option_list import Option

from ...data import Bookmark, load_bookmarks
from .navigation_pane import NavigationPane


class Entry(Option):
    """An entry in the bookmark list."""

    def __init__(self, bookmark: Bookmark) -> None:
        super().__init__(self._as_prompt(bookmark))
        self.bookmark = bookmark
        """The bookmark that this entry relates to."""

    @staticmethod
    def _as_prompt(bookmark: Bookmark) -> Text:
        """Depict the bookmark as a decorated prompt.

        Args:
            bookmark: The bookmark to depict.

        Returns:
            A prompt with icon, etc.
        """
        return Text.from_markup(
            f":{'page_facing_up' if isinstance(bookmark.location, Path) else 'globe_with_meridians'}: "
            f"[bold]{bookmark.title}[/]\n[dim]{bookmark.location}[/]",
            overflow="ellipsis",
        )


class Bookmarks(NavigationPane):
    """Bookmarks navigation pane."""

    DEFAULT_CSS = """
    Bookmarks {
        height: 100%;
    }

    Bookmarks > OptionList {
        background: $primary;
    }
    """

    def __init__(self) -> None:
        """Initialise the bookmarks navigation pane."""
        super().__init__("Bookmarks")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield OptionList()

    def on_mount(self) -> None:
        """Load up the bookmarks once the DOM is ready."""
        bookmarks = self.query_one(OptionList)
        for bookmark in load_bookmarks():
            bookmarks.add_option(Entry(bookmark))

    def set_focus_within(self) -> None:
        """Focus the option list."""
        self.query_one(OptionList).focus()

    class Goto(Message):
        """Message that requests that the viewer goes to a given bookmark."""

        def __init__(self, bookmark: Bookmark) -> None:
            """Initialise the bookmark goto message.

            Args:
                bookmark: The bookmark to go to.
            """
            super().__init__()
            self.bookmark = bookmark

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle an entry in the bookmarks being selected.

        Args:
            event: The event to handle.
        """
        event.stop()
        assert isinstance(event.option, Entry)
        self.post_message(self.Goto(event.option.bookmark))
