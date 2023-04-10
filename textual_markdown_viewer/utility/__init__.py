"""General utility and support code."""

from .config import Config, load_config, save_config
from .type_tests import maybe_markdown, is_likely_url

__all__ = ["maybe_markdown", "is_likely_url", "load_config", "save_config", "Config"]
