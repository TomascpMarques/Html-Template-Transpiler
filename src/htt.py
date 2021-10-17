"""
O ponto inicial do programa
"""

# import sys
# from cmd_module.cmd import parse_cmd_args
import sys
from cmd_module.cmd import Cmd, CmdArgument
from cmd_module.args_disp import CMD_ARGS


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """
    # some = parse_cmd_args(sys.argv)
    # print(some)

    # template for sys args, besides type

    cmd = Cmd(CMD_ARGS)
    cmd.parse_cmd_args(sys.argv)


if __name__ == '__main__':
    main()
