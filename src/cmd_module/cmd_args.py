"""
Contêm os argumentos disponíveis para uso pela cmd
"""

from cmd_module.cmd_arg_resolvers.cmd_arg_setup import CmdArgumento
from cmd_module.cmd_arg_resolvers.file_arg_resolver import file as FILE_ARG


CMD_ARGS: dict[str, CmdArgumento] = {
    'file': FILE_ARG,
}
