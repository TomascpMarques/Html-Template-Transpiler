"""
Cli global store
"""

from typing import Any, TypeVar

SomeType = TypeVar('SomeType')

CLI_STORE: dict[str, Any] = {
    'htt-config': '.httconfig',
}


def cli_store_set(key: str, value: SomeType) -> SomeType:
    """
    Sets a value in the store.
    """

    CLI_STORE.__setitem__(key, value)
    return value


def cli_store_update(key: str, value: SomeType) -> SomeType:
    """
    Updates a value in the store if key already exists.
    Else creates a new key/value pair.
    """
    if key not in CLI_STORE:
        return cli_store_set(key, value)

    return cli_store_set(
        key,
        CLI_STORE[key].update(value)
    )


def cli_store_get(key: str) -> Any | None:
    """
    Gets a value from the store.
    """
    return CLI_STORE.get(key)
