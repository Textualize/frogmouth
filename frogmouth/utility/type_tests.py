"""Support code for testing files for their potential type."""

from functools import singledispatch
from pathlib import Path
from typing import Any

from httpx import URL

from ..data.config import load_config


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
    return resource.suffix.lower() in load_config().markdown_extensions


@maybe_markdown.register
def _(resource: str) -> bool:
    return maybe_markdown(Path(resource))


@maybe_markdown.register
def _(resource: URL) -> bool:
    return maybe_markdown(resource.path)


def is_likely_url(candidate: str) -> bool:
    """Does the given value look something like a URL?

    Args:
        candidate: The candidate to check.

    Returns:
        `True` if the string is likely a URL, `False` if not.
    """
    # Quick and dirty for now.
    url = URL(candidate)
    return url.is_absolute_url and url.scheme in ("http", "https")
