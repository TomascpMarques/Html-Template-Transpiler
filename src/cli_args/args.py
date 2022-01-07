"""
Contêm os argumentos disponíveis para uso pela cli
"""

# Other imports
import re

# Program Modules
from cli.arg_setup import CliArgumento
from cli.erros import erro_exit
from cli_args.file_resolver import files_arg
from cli_args.config_resolver import config_arg
from cli_args.hotreload_resolver import hotreload_arg


def resolver_cli_args(arg: str, param: str) -> None:
    """
    Resolve o argumento da cli especificado com o param dados

    Args:
        arg (str): Argumento a ser resolvidores
        param (any): Parametro a fornecer ao argumento
    """
    # Corre um argumento (dos disponiveis) com o parametro fornecido
    CLI_ARGS[arg].run(param)


def run_arg_help(arg: str) -> None:
    """
    Fornece ajuda sobre um argumento

    Args:
        arg (str): Ajuda sobre o argumento pedido
    """
    # 'all' irá devolver todas as ajudas disponiveis sobre todos os argumentos
    if arg == 'all':
        print('Help:')
        for args, val in CLI_ARGS.items():
            print(
                f' --{args}:{" "*2}{val.descricao_argumento}')
        return

    # Ajuda pedida sobre um argumento não existente
    # IRá devolver um erro
    if arg not in CLI_ARGS.keys():
        erro_exit(
            menssagen="O argumento dado não existe",
            time_stamp=True,
            tipo_erro="ArgInvalErr"
        )

    ajuda_arg = CLI_ARGS[arg].mensagem_ajuda
    desc_arg = CLI_ARGS[arg].descricao_argumento
    print(
        f'Ajuda:\n{ajuda_arg}\n{"~ "*(len(ajuda_arg)//4)}\nDescrição do argumento:\n -> {desc_arg}'
    )


help_mens_ajuda: str = '* Parametro: <help> | Exemplo: --help file'

help_arg: CliArgumento = CliArgumento(
    chave='help',
    run=run_arg_help,
    descricao_argumento='Argumento de ajuda com um ou mais argumentos',
    erro_validacao='O valor deve ser uma key de argumento válida',
    mensagem_ajuda=help_mens_ajuda,
    re_validacao_tipo_valor=re.compile('[a-z]+'),
    func_validacao=lambda x: x.isalpha()
)

# program args
CLI_ARGS: dict[str, CliArgumento] = {
    'files': files_arg,
    'config': config_arg,
    'help': help_arg,
    'hotreload': hotreload_arg,
}
