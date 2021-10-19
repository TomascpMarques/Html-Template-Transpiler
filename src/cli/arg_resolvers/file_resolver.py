"""
Desenvolvimento e resolving do argumento file
"""

import re


from cli.arg_resolvers.arg_setup import CliArgumento

file: CliArgumento = CliArgumento(
    chave='file',
    descricao_argumento='O ficheiro de template a transpilar',
    erro_validacao='Não foi possivél validar o valor para o argumento <file>',
    re_validacao_tipo_valor=re.compile(
        r'(\.\/|\/)(\w+\/)+\w+\.\w+|\.\/\w+\.\w+'),
)
