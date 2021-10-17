"""
O ponto inicial do programa
"""

# import sys
# from cmd_module.cmd import parse_cmd_args
from cmd_module.cmd import Cmd, CmdArgument


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """
    # some = parse_cmd_args(sys.argv)
    # print(some)

    # template for sys args, besides type

    arg = [CmdArgument('b', float)]
    cmd = Cmd(arg)
    print(f'->{cmd.arguments=}')


if __name__ == '__main__':
    main()
