"""
Setup e criação de argumentos aceitaiveis pela cli
"""

# Other Imports
import re
from typing import Callable
from dataclasses import dataclass, field

# Project Modules
from cli.erros import erro_exit


@dataclass()
class CliArgumento():
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cli
    """
    # Resolve o argumento chamado com o valor fornecido
    run: Callable = field()
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
    validacao_arg_passado: re.Pattern | Callable = field(
        default=re.compile('')
    )
    erro_validacao: str = field(
        default='Erro: Não foi possível validar o valor fornecido para um ou mais argumentos'
    )
    mensagem_ajuda: str = field(
        default="O campo pode tomar valor <MODIFICAR AQUI>"
    )


def validar_argumento(campo: CliArgumento, arg: str) -> str:
    """
    Valida um argumento com o seu regex de validação

    Returns:
        str | None : String (em caso de bom valor) ou None (em caso de erro)
    """
    if isinstance(campo.validacao_arg_passado, re.Pattern):
        if not campo.validacao_arg_passado.match(arg):
            erro_exit(
                time_stamp=True,
                tipo_erro="Err_Arg_Validcao",
                menssagen=campo.erro_validacao,
            )
    else:
        if not campo.validacao_arg_passado(arg):
            erro_exit(
                time_stamp=True,
                tipo_erro="Err_Arg_Validcao",
                menssagen=campo.erro_validacao,
            )
    return campo.func_validacao(arg)
