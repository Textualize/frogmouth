"""Provides the bookmarks navigation pane."""

from .navigation_pane import NavigationPane


class Bookmarks(NavigationPane):
    """Bookmarks navigation pane."""

    def __init__(self) -> None:
        """Initialise the bookmarks navigation pane."""
        super().__init__("Bookmarks")
