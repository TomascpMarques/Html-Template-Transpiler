"""
Desenvolvimento e resolving do argumento <files> (--files)
"""

# Other imports
import re
from typing import Any

# Program Modules
from cli.arg_setup import CliArgumento
from cli_store.store import cli_store_get, cli_store_set
from file_templating.templater import HTT_CONFIG_FILE, Templater


def run_arg_files(path_ficheiros: str, **_kwargs: Any) -> None:
    """
    Resolve o argumento para lidar com os ficheiros
    fornecidos para criar o projeto

    Args:
        path_ficheiros (str): Caminho até à pasta que fornece os ficheiros alvo
    """
    config_path: str = ''

    # Default check for custom config files
    if cli_store_get('htt-config') is not None:
        config_path = str(
            cli_store_get('htt-config')
        )
        # Default config file fallback, on by default
        if HTT_CONFIG_FILE != config_path:
            cli_store_set(
                'htt-config-fallback',
                HTT_CONFIG_FILE
            )
        else:
            cli_store_set(
                'htt-config-fallback',
                None
            )
    else:
        # If no custom config file is set
        # Defaults for the "general" htt-config file path
        config_path = HTT_CONFIG_FILE

    # Set project directorie
    cli_store_set('htt-project', path_ficheiros)

    # Init o processo de templating com os ficheiros fornecidos
    project_templater = Templater(
        path=path_ficheiros,
        config_file_path=config_path
    )

    print('Ficheiros (.htt) utilizados:')
    for ficheiro in project_templater.templating.htt_templates:
        print(f'|  -> {ficheiro}')
    print('-'*20)
    print('Feito!')


files_mens_ajuda: str = \
    '* Parametro: <files> | Exemplo: --files ./alguma/pasta\n\
O argumento têm que apontar para uma pasta válida'

files_arg: CliArgumento = CliArgumento(
    chave='files',
    run=run_arg_files,
    descricao_argumento='O ficheiro de template a transpilar',
    erro_validacao='Não foi possivél validar o valor para o argumento <files>',
    mensagem_ajuda=files_mens_ajuda,
    re_validacao_tipo_valor=re.compile(
        r'^(\.{1,2}\/|\~{1}\/|\/)\S+\/$|^[A-z_-]+\/'
    ),
)
