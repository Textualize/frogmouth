"""Support code for testing files for their potential type."""

from __future__ import annotations

from functools import singledispatch
from pathlib import Path
from typing import Any

from httpx import URL, AsyncClient, HTTPStatusError, RequestError

from ..utility.advertising import USER_AGENT
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
async def _(resource: URL) -> bool:
    async with AsyncClient() as client:
        try:
            response = await client.head(
                resource,
                follow_redirects=True,
                headers={"user-agent": USER_AGENT},
            )
            response.raise_for_status()
        except (RequestError, HTTPStatusError) as error:
            # We've failed to even make the request, there's no point in
            # trying to build anything here.
            return False
    return maybe_markdown(response.url.path)


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
