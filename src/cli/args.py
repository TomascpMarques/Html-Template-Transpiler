"""
Contêm os argumentos disponíveis para uso pela cli
"""

from cli.arg_resolvers.arg_setup import CliArgumento
from cli.arg_resolvers.file_resolver import file as FILE_ARG


CLI_ARGS: dict[str, CliArgumento] = {
    'file': FILE_ARG,
}


def resolver_cli_args(arg: str, param: any) -> None:
    """
    Resolve o argumento da cli especificado com o param dados

    Args:
        arg (str): Argumento a ser resolvidores
        param (any): Parametro a fornecer ao argumento
    """
    CLI_ARGS[arg].run(param)
