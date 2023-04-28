"""Provides the table of contents navigation pane."""

from textual.app import ComposeResult
from textual.widgets import Markdown, Tree
from textual.widgets.markdown import MarkdownTableOfContents

from .navigation_pane import NavigationPane


class TableOfContents(NavigationPane):
    """Markdown document table of contents navigation pane."""

    DEFAULT_CSS = """
    TableOfContents {        
        height: 100%;        
    }

    TableOfContents > MarkdownTableOfContents {
        background: $panel;
        border: none;
    }

    TableOfContents > MarkdownTableOfContents > Tree {
        width: 1fr;
        background: $panel;
        padding: 0;
    }

    TableOfContents > MarkdownTableOfContents > Tree:focus .tree--cursor, TableOfContents > MarkdownTableOfContents > Tree .tree--cursor {
        background: $accent 50%;
        color: $text;
    }
    """

    def __init__(self) -> None:
        """Initialise the table of contents navigation pane."""
        super().__init__("Contents")

    def compose(self) -> ComposeResult:
        """Compose the child widgets."""
        yield MarkdownTableOfContents()

    def on_table_of_contents_updated(
        self, event: Markdown.TableOfContentsUpdated
    ) -> None:
        """Handle a table of contents update event.

        Args:
            event: The table of content update event to handle.
        """
        self.query_one(
            MarkdownTableOfContents
        ).table_of_contents = event.table_of_contents
