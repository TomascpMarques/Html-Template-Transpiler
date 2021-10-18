"""
O ponto inicial do programa
"""

# import sys
# from cmd_module.cmd import parse_cmd_args
import sys
from cmd_module.cmd import Cmd, CmdArgumento
from cmd_module.cmd_args import CMD_ARGS, validar_argumento
import re


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """

    # template for sys args, besides type

    CMD = Cmd(**CMD_ARGS)
    CMD.parse_cmd_args(sys.argv)
    print(f'{CMD.argumentos=}')

    t = CmdArgumento(
        chave='t',
        func_valida=lambda x: int(x),
        re_validacao_tipo_valor=re.compile('^\d+$')
    )

    x = validar_argumento(t, '132')
    print(x, type(x))


if __name__ == '__main__':
    main()
