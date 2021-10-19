"""
Contêm os argumentos disponíveis para uso pela cli
"""

from cli.arg_resolvers.arg_setup import CliArgumento
from cli.arg_resolvers.file_resolver import file as FILE_ARG


CLI_ARGS: dict[str, CliArgumento] = {
    'file': FILE_ARG,
}
