"""General utility and support code."""

from .forge import (
    build_raw_bitbucket_url,
    build_raw_codeberg_url,
    build_raw_github_url,
    build_raw_gitlab_url,
)
from .type_tests import is_likely_url, maybe_markdown

__all__ = [
    "build_raw_bitbucket_url",
    "build_raw_codeberg_url",
    "build_raw_github_url",
    "build_raw_gitlab_url",
    "is_likely_url",
    "maybe_markdown",
]
