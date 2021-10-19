"""
O ponto inicial do programa
"""

import sys

from cmd_module.cmd import CmdListner
from cmd_module.cmd_args import CMD_ARGS


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """

    # template for sys args, besides type

    running_cmd = CmdListner(**CMD_ARGS)
    running_cmd.parse_cmd_args(sys.argv)
    print(f'{running_cmd.argumentos=}')


if __name__ == '__main__':
    main()
