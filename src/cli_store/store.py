"""
Cli global store
"""

from typing import Any

CLI_STORE: dict[str, Any] = {
    'htt-config': '.httconfig',
}


def cli_store_set(key: str, value: Any) -> Any:
    """
    Sets a value in the store.
    """

    CLI_STORE.__setitem__(key, value)
    return value


def cli_store_get(key: str) -> Any | None:
    """
    Gets a value from the store.
    """
    return CLI_STORE.get(key)
