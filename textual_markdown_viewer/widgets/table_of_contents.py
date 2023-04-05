"""Provides the table of contents navigation pane."""

from textual.app import ComposeResult
from textual.widgets import Markdown, TabPane
from textual.widgets.markdown import MarkdownTableOfContents


class TableOfContents(TabPane):
    """Markdown document table of contents navigation pane."""

    DEFAULT_CSS = """
    TableOfContents {
        height: 100%;
    }

    TableOfContents > MarkdownTableOfContents {
        background: $primary;
        border: none;
    }

    TableOfContents > MarkdownTableOfContents > Tree {
        background: $primary;
        padding: 0;
    }
    """

    def __init__(self) -> None:
        """Initialise the table of contents navigation pane."""
        super().__init__("Contents")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield MarkdownTableOfContents()

    def on_table_of_contents_updated(self, event: Markdown.TableOfContentsUpdated):
        """Handle a table of contents update event.

        Args:
            event: The table of content update event to handle.
        """
        self.query_one(
            MarkdownTableOfContents
        ).table_of_contents = event.table_of_contents
