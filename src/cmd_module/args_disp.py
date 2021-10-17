"""
Contêm os argumentos disponíveis para uso pela cmd
"""

from cmd_module.cmd import CmdArgument


CMD_ARGS: list[CmdArgument] = [
    CmdArgument('file', str),
    CmdArgument('s', str)
]
