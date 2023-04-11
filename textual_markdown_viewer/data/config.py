"""Provides code for loading/saving configuration."""

from dataclasses import asdict, dataclass
from json import dumps, loads
from pathlib import Path

from xdg import xdg_config_home

from ..utility.advertising import ORGANISATION_NAME, PACKAGE_NAME


@dataclass
class Config:
    """The markdown viewer configuration."""

    light_mode: bool = False
    """Should we run in light mode?"""


def config_file() -> Path:
    """Get the path to the configuration file.

    Returns:
        The path to the configuration file.

    Note:
        As a side effect the configuration directory will be created if it
        does not exist.
    """
    (config_dir := xdg_config_home() / ORGANISATION_NAME / PACKAGE_NAME).mkdir(
        parents=True, exist_ok=True
    )
    return config_dir / "configuration.json"


def save_config(config: Config) -> None:
    """Save the given configuration to storage.

    Args:
        config: The configuration to save.
    """
    config_file().write_text(dumps(asdict(config), indent=4))


def load_config() -> Config:
    """Load the configuration from storage.

    Returns:
        The configuration.
    """
    source_file = config_file()
    return (
        Config(**loads(source_file.read_text())) if source_file.exists() else Config()
    )
