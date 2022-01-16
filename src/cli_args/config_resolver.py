"""
Resolver o parametro config do programa,
para quando o ficheiro de config se encontra em um local
que não é o mesmo dos ficheiros.
"""

# Other modules
import os
from typing import Any
import requests

# Program Modules
from cli.arg_setup import CliArgumento
from cli_store.store import cli_store_set


def run_arg_config(path_config: str, **__kwargs: Any) -> None:
    """
    Resolve o argumento para lidar com path
    para o ficheiro de config

    Args:
        path_config (str): Path ou link para o ficheiro
        de config para o projeto
    """
    print(f'A utilizar o file de config:\n -> «{path_config}»')
    cli_store_set(
        'htt-config',
        path_config
    )


config_mens_ajuda: str = \
    '* Parametro: <config> | Exemplo: --config ./alguma/pasta/.httconfig <ou>' + \
    'https: // some.foo.bar/.httconfig\nO argumento têm que apontar para uma pasta válida'


def validar_config_filepath(path: str) -> bool:
    """
    Valida se o ficheiro de config fornecido
    é um path existente no sistema, ou se aponta
    para o ficheiro de config num repositorio
    """
    if not os.path.exists(path):
        exists_web: requests.Response = requests.get(
            f'https://raw.githubusercontent.com/{path}'
        )
        if exists_web.status_code != 200:
            return False

    return True


config_arg: CliArgumento = CliArgumento(
    chave='config',
    run=run_arg_config,
    descricao_argumento='O path do ficheiro de configurações do projeto',
    erro_validacao='Não foi possivél validar o valor para o argumento <config>',
    mensagem_ajuda=config_mens_ajuda,
    validacao_arg_passado=validar_config_filepath,
)
