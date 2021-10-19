"""
Setup e criação de argumentos aceitaiveis pela cli
"""

import re
from dataclasses import dataclass, field
from typing import Callable

from cli.erros import erro_exit


@dataclass
class CliArgumento():
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cli
    """
    func_validacao: Callable = field(default=lambda x: x)
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
        default='Erro: Não foi possível validar o valor fornecido para um ou mais argumentos'
    )


def validar_argumento(campo: CliArgumento, arg: str) -> str | None:
    """Valida um argumneto contra o seu regex de validação

    Returns:
        [type]: [description]
    """
    if not campo.re_validacao_tipo_valor.match(arg):
        erro_exit(
            time_stamp=True,
            tipo_erro="Err_Arg_Validcao",
            menssagen=campo.erro_validacao,
        )
        return None
    return campo.func_validacao(arg) or arg
