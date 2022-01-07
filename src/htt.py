"""
O ponto inicial do programa
"""

import sys

from cli.cli import Cli
from cli_args.args import CLI_ARGS


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script.
    """
    program_cli = Cli(sys.argv, **CLI_ARGS)
    program_cli.run()


if __name__ == '__main__':
    main()
