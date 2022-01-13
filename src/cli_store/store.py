"""
Cli global store - Not multi-threaded safe.
Might have race conditions when multi-threaded.
"""

from typing import Any, TypeVar

GeneralType = TypeVar('GeneralType')

CLI_STORE: dict[str, Any] = {
    # Default htt-config settings
    'htt-config': '.httconfig',
}


def cli_store_set(key: str, value: GeneralType) -> GeneralType:
    """
    Sets a value in the program global store.
    """

    CLI_STORE.__setitem__(key, value)
    return value


def cli_store_get(key: str) -> Any | None:
    """
    Gets a value from the programs global store.
    """
    return CLI_STORE.get(key)
