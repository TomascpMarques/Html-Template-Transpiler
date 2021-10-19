"""
O ponto inicial do programa
"""

import sys

from cli.cli import CliListner
from cli.args import CLI_ARGS


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """

    # template for sys args, besides type

    running_cli = CliListner(**CLI_ARGS)
    running_cli.parse_cli_args(sys.argv)
    print(f'{running_cli.argumentos=}')


if __name__ == '__main__':
    main()
