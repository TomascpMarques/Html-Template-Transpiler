"""
Contêm os argumentos disponíveis para uso pela cmd
"""


from dataclasses import dataclass, field
import re
import sys
from typing import Generic, Type, TypeVar


@dataclass
class CmdArgumento():
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cmd
    """
    func_valida: any = field(default=lambda x: x)
    chave: str = field(
        default_factory=str
    )
    descricao_argumento: str = field(
        default_factory=str
    )
    re_validacao_tipo_valor: re.Pattern = field(
        default=re.compile('')
    )
    erro_validacao: str = field(
        default=f'Erro: Não foi possível validar o valor fornecido para um ou mais argumentos'
    )


def validar_argumento(campo: CmdArgumento, arg: str) -> any:
    if not campo.re_validacao_tipo_valor.match(arg):
        sys.exit(campo.erro_validacao)
    else:
        return campo.func_valida(arg) or arg


__file: CmdArgumento = CmdArgumento(
    chave='file',
    descricao_argumento='O ficheiro de template a transpilar',
    erro_validacao='Erro: não foi possivél validar o valor para o argumento <file>',
    re_validacao_tipo_valor=re.compile(
        '(\.\/|\/)(\w+\/)+\w+\.\w+|\.\/\w+\.\w+'),
)

CMD_ARGS: dict[str, CmdArgumento] = {
    'file': __file,
}
