"""The markdown viewer itself."""

from pathlib import Path

from httpx import AsyncClient, URL

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Markdown

from .. import __version__

PLACEHOLDER = """\
# Textual Markdown Viewer

Welcome to the Textual Markdown viewer!
"""


class Viewer(VerticalScroll, can_focus=True, can_focus_children=True):
    """The Markdown viewer class."""

    def compose(self) -> ComposeResult:
        """Compose the markdown viewer."""
        yield Markdown(PLACEHOLDER)

    @property
    def document(self) -> Markdown:
        """The markdown document."""
        return self.query_one(Markdown)

    async def _remote_load(self, location: URL) -> None:
        """Load a Markdown document from a URL.

        Args:
            location: The location to load from.
        """
        async with AsyncClient() as client:
            response = await client.get(
                location,
                follow_redirects=True,
                headers={"user-agent": f"textual-markdown-client v{__version__}"},
            )
            # TODO: Lots of error handling.
            self.document.update(response.text)

    async def visit(self, location: Path | URL) -> None:
        """Visit a location.

        Args:
            location: The location to visit.
        """
        if isinstance(location, Path):
            await self.document.load(location)
        elif isinstance(location, URL):
            await self._remote_load(location)
        else:
            raise ValueError("Unknown location type passed to the Markdown viewer")
        # TODO: add the location to the history.
