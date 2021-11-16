"""
Desenvolvimento e resolving do argumento <files> (--files)
"""

# Other imports
import re
from typing import Any

# Program Modules
from cli.arg_setup import CliArgumento
from file_templating.templater import HTT_CONFIG_FILE, Templater


def run_arg_files(path_ficheiros: str, **kwargs: Any) -> None:
    """
    Resolve o argumento para lidar com os ficheiros dados

    Args:
        path_ficheiros (str): Caminho até à pasta que fornece os ficheiros alvo
    """
    config_path: str = ''
    if kwargs.get('htt-config') is not None:
        config_path = kwargs['htt-config']
    else:
        config_path = HTT_CONFIG_FILE

    # Init o processo de templating com os ficheiros fornecidos
    project_templater = Templater(
        path=path_ficheiros,
        config_file_path=(
            config_path
        )
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
    erro_validacao='Não foi possivél validar o valor para o argumento <file>',
    mensagem_ajuda=files_mens_ajuda,
    re_validacao_tipo_valor=re.compile(
        r'(^\.\.\/|^\.\/|^\.)|(^\.\/|^\.|^~\/|^\/)(\w+\/)+'
    ),
)
