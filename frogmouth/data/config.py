"""Provides code for loading/saving configuration."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from functools import lru_cache
from json import dumps, loads
from pathlib import Path

from xdg import xdg_config_home

from ..utility.advertising import ORGANISATION_NAME, PACKAGE_NAME


@dataclass
class Config:
    """The markdown viewer configuration."""

    light_mode: bool = False
    """Should we run in light mode?"""

    markdown_extensions: list[str] = field(default_factory=lambda: [".md", ".markdown"])
    """What Markdown extensions will we look for?"""

    navigation_left: bool = True
    """Should navigation be docked to the left side of the screen?"""


def config_file() -> Path:
    """Get the path to the configuration file.

    Returns:
        The path to the configuration file.

    Note:
        As a side-effect, the configuration directory will be created if it
        does not exist.
    """
    (config_dir := xdg_config_home() / ORGANISATION_NAME / PACKAGE_NAME).mkdir(
        parents=True, exist_ok=True
    )
    return config_dir / "configuration.json"


def save_config(config: Config) -> Config:
    """Save the given configuration to storage.

    Args:
        config: The configuration to save.

    Returns:
        The configuration.
    """
    # Ensure any cached copy of the config is cleaned up.
    load_config.cache_clear()
    # Dump the given config to storage.
    config_file().write_text(dumps(asdict(config), indent=4))
    # Finally, load it up again. This is to make sure that the updated
    # version is in the cache.
    return load_config()


@lru_cache(maxsize=None)
def load_config() -> Config:
    """Load the configuration from storage.

    Returns:
        The configuration.

    Note:
        As a side-effect, if the configuration doesn't exist a default one
        will be saved to storage.

        This function is designed so that it's safe and low-cost to
        repeatedly call it. The configuration is cached and will only be
        loaded from storage when necessary.
    """
    source_file = config_file()
    return (
        Config(**loads(source_file.read_text()))
        if source_file.exists()
        else save_config(Config())
    )
