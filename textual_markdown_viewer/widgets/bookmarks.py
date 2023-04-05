"""Provides the bookmarks navigation pane."""

from textual.widgets import TabPane


class Bookmarks(TabPane):
    """Bookmarks navigation pane."""

    def __init__(self) -> None:
        """Initialise the bookmarks navigation pane."""
        super().__init__("Bookmarks")
