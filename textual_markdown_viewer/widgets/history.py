"""Provides the history navigation pane."""

from pathlib import Path

from httpx import URL

from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import TabPane, OptionList
from textual.widgets.option_list import Option


class Entry(Option):
    """An entry in the history."""

    def __init__(self, location: Path | URL) -> None:
        """Initialise the history entry item.

        Args:
            location: The location being added to history.
        """
        super().__init__(str(location))
        self.location = location
        """The location for his entry in the history."""


class History(TabPane):
    """History navigation pane."""

    DEFAULT_CSS = """
    History {
        height: 100%;
    }

    History > OptionList {
        background: $primary;
    }
    """

    def __init__(self) -> None:
        """Initialise the history files navigation pane."""
        super().__init__("History")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield OptionList()

    def add(self, location: Path | URL) -> None:
        """Add a new location to the history.

        Args:
            location: The location to add.
        """
        self.query_one(OptionList).add_option(Entry(location))

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

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle an entry in the history being selected.

        Args:
            event: The event to handle.
        """
        event.stop()
        assert isinstance(event.option, Entry)
        self.post_message(self.Goto(event.option.location))
