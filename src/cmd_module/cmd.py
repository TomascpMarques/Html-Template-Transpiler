"""
Modulo relativo à interação do user com o programa através do terminal
"""

import sys
import re
from dataclasses import dataclass, field


@dataclass
class CmdArgument:
    key: str = field(default_factory=str)
    value_type: type = field(default_factory=str)
    validation_template: re.Pattern = field(default=re.compile('--\w+\s'))


class Cmd:
    def __init__(self, args: 'list[CmdArgument]'):
        self.arguments: dict[str, CmdArgument] = dict(
            (argumet.key, argumet) for argumet in args
        )


def parse_cmd_args(args: 'list[str]') -> dict:
    """Parse os argurmentos dados ao correr o script

    Args:
        args(list[str]): Os argumentos usados ao correr o script

    Returns:
        dict: Os argumentos usados em formato de dicionario
    """

    # Ignora o primeiro elemento dos argumentos - o nome/path do ficheiro
    del args[0]

    # Verifica se existem argumentos, retorna "help" do script
    if args.__len__() < 3:
        # Temporário
        sys.exit('O programa deve ser chamado com pelo menos 1 argumento e valor')

    # Verifica argumentos sem valor, mas defenidos
    if args.__len__() % 2 != 0:
        sys.exit('Erro: Todos os argumentos chamados devem ter valores associados')

    # retira as keys dos argumentos
    keys_args: list[str] = []
    values_args: list[str] = []

    for item in args:
        if re.compile(r'--\w+').match(item) is not None:
            # Ignora os simbolos pre chave ex: "(--)chave"
            keys_args.append(item[2:])
        else:
            values_args.append(item)

    return dict(zip(keys_args, values_args))
