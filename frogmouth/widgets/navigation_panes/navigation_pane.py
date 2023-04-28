"""Provides a base class for all navigation panes."""

from textual.widgets import TabbedContent, TabPane


class NavigationPane(TabPane):
    """Base class for panes within the navigation sidebar."""

    def set_focus_within(self) -> None:
        """Set the focus on the correct child within."""

    def activate(self) -> None:
        """Activate the navigation pane."""
        assert self.parent is not None
        if self.id is not None and isinstance(self.parent.parent, TabbedContent):
            self.parent.parent.active = self.id
