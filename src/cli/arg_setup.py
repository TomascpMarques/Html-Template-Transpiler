"""
Setup e criação de argumentos aceitaiveis pela cli
"""

# Other Imports
import re
from typing import Callable
from dataclasses import dataclass, field

# Project Modules
from cli.erros import erro_exit


# A utilização de slots permite poupar memóriacom os atribts. da class
@dataclass(slots=True)
class CliArgumento():
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cli
    """
    # Resolve o argumento chamado com o valor fornecido
    run: Callable = field(
        default=lambda x: x
    )
    # Irá validar o valor dado ao argumento na cli
    func_validacao: Callable = field(
        default=lambda x: x
    )
    # Identificação do argumento dentro do programa
    chave: str = field(
        default_factory=str
    )
    descricao_argumento: str = field(
        default_factory=str
    )
    # Regex para validar o tipo de dado do valor recebido
    re_validacao_tipo_valor: re.Pattern = field(
        default=re.compile('')
    )
    erro_validacao: str = field(
        default='Erro: Não foi possível validar o valor fornecido para um ou mais argumentos'
    )
    mensagem_ajuda: str = field(
        default="O campo pode tomar valor x"
    )


def validar_argumento(campo: CliArgumento, arg: str) -> str | None:
    """
    Valida um argumento com o seu regex de validação

    Returns:
        str | None : String (em caso de bom valor) ou None (em caso de erro)
    """
    if not campo.re_validacao_tipo_valor.match(arg):
        erro_exit(
            time_stamp=True,
            tipo_erro="Err_Arg_Validcao",
            menssagen=campo.erro_validacao,
        )
        return None
    return campo.func_validacao(arg)
