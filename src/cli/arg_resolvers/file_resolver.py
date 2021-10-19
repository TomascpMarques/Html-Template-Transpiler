"""
Desenvolvimento e resolving do argumento file
"""

import re

from cli.arg_resolvers.arg_setup import CliArgumento


def run_arg_file(path_ficheiro: str):
    """
    some some here
    """
    with open(
        file=path_ficheiro,
        mode='r',
        encoding='utf-8'
    ) as ficheiro:
        print(f'{ficheiro.read()=}')


file: CliArgumento = CliArgumento(
    chave='file',
    run=run_arg_file,
    descricao_argumento='O ficheiro de template a transpilar',
    erro_validacao='Não foi possivél validar o valor para o argumento <file>',
    re_validacao_tipo_valor=re.compile(
        r'(\.\/|\/|~\/)(\w+\/)+\w+\.\w+|\.\/\w+\.\w+'),
)
