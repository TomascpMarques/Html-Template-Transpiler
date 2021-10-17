"""
O ponto inicial do programa
"""

# import sys
# from cmd_module.cmd import parse_cmd_args
import sys
from cmd_module.cmd import Cmd, CmdArgument


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """
    # some = parse_cmd_args(sys.argv)
    # print(some)

    # template for sys args, besides type

    arg = [CmdArgument('file', str), CmdArgument('s', str)]
    cmd = Cmd(arg)
    cmd.parse_cmd_args(sys.argv)


if __name__ == '__main__':
    main()
