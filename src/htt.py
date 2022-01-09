"""
O ponto inicial do programa
"""

import os
import sys

from cli.cli import Cli
from cli_args.args import CLI_ARGS
from cli_store.store import cli_store_set


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script.
    """
    cli_store_set('base_path', os.getcwd())
    program_cli = Cli(sys.argv, **CLI_ARGS)
    program_cli.run()


if __name__ == '__main__':
    main()
