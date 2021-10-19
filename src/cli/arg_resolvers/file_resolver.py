"""
Desenvolvimento e resolving do argumento file
"""

import re

from cli.arg_resolvers.arg_setup import CliArgumento


def run_arg_file():
    """
    some some here
    """
    print(f'Hello my friend super cool: {2*2}')


file: CliArgumento = CliArgumento(
    chave='file',
    run=run_arg_file,
    descricao_argumento='O ficheiro de template a transpilar',
    erro_validacao='Não foi possivél validar o valor para o argumento <file>',
    re_validacao_tipo_valor=re.compile(
        r'(\.\/|\/)(\w+\/)+\w+\.\w+|\.\/\w+\.\w+'),
)
