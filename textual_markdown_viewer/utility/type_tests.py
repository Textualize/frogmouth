"""Support code for testing if files for their potential type."""

from functools import singledispatch
from pathlib import Path
from typing import Any

from httpx import URL


@singledispatch
def maybe_markdown(resource: Any) -> bool:
    """Does the given resource look like it's a Markdown file?

    Args:
        resource: The resource to test.

    Returns:
        `True` if the resources looks like a Markdown file, `False` if not.
    """
    del resource
    return False


@maybe_markdown.register
def _(resource: Path) -> bool:
    return resource.suffix.lower() == ".md"


@maybe_markdown.register
def _(resource: str) -> bool:
    return maybe_markdown(Path(resource))


@maybe_markdown.register
def _(resource: URL) -> bool:
    return maybe_markdown(resource.path)
