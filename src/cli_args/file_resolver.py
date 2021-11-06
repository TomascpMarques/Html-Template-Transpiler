"""
Desenvolvimento e resolving do argumento file
"""

import re

from cli.arg_setup import CliArgumento
from file_templating.templater import Templater


def run_arg_files(path_ficheiros: str) -> None:
    """
    Resolve o argumento para lidar com os ficheiros dados

    Args:
        path_ficheiros (str): Caminho até à pasta que fornece os ficheiros alvo
    """
    print("-><<<<<", path_ficheiros)
    Templater(path=path_ficheiros)


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
