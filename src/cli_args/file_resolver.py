"""
Desenvolvimento e resolving do argumento file
"""

import re

from cli.arg_setup import CliArgumento
from file_handeling.handler import FileHandler


def run_arg_files(path_ficheiros: str) -> None:
    """
    some some here
    """
    some = FileHandler(path_ficheiros)
    print(some.resolver_ficheiro('.httconfig'))


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
