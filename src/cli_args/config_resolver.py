"""
Resolver o parametro <--config>,
para quando o ficheiro de config se encontra em outro local
"""
import re
from typing import Any

from cli.arg_setup import CliArgumento
from cli_store.store import cli_store_set


def run_arg_config(path_config: str, **__kwargs: Any) -> None:
    """
    Resolve o argumento para lidar com path para o ficheiro
    de config

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

config_arg: CliArgumento = CliArgumento(
    chave='config',
    run=run_arg_config,
    descricao_argumento='O path do ficheiro de configurações do projeto',
    erro_validacao='Não foi possivél validar o valor para o argumento <config>',
    mensagem_ajuda=config_mens_ajuda,
    re_validacao_tipo_valor=re.compile(
        r'^(~\/|\.{1,2}\/|\/)([A-z_-]+\/){1,}\.httconfig$' +
        r'|\S+$'
    ),
)
