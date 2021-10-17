"""
Modulo relativo à interação do user com o programa através do terminal
"""

import sys
import re
from dataclasses import dataclass, field


@dataclass
class CmdArgument:
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cmd
    """
    key: str = field(default_factory=str,)
    value_type: type = field(default_factory=str)
    validation_template: re.Pattern = field(default=re.compile('--\w+\s'))


class Cmd:
    """
    Propiedades da cmd/interação do user com a aplicação,
    contêm os argumentos disponiveis, e valida e interage
    com os pedidos do utilizador
    """

    def __init__(self, args: 'list[CmdArgument]'):
        self.argumentos: dict[str, CmdArgument] = dict(
            (argumet.key, argumet) for argumet in args
        )

    def parse_cmd_args(self, args: 'list[str]') -> dict:
        """Parse os argurmentos dados ao correr o script

        Args:
            args(list[str]): Os argumentos usados ao correr o script

        Returns:
            dict: Os argumentos usados em formato de dicionario
        """

        # pre validação dos argumentos dados
        self.args_list_pre_validation(args)

        # retira as keys dos argumentos
        keys_args: list[str] = []
        values_args: list[str] = []

        for item in args:
            if re.compile(r'--\w+').match(item) is not None:
                # item[2:] -> Ignora os simbolos pre chave ex: "(--)chave"
                if self.arg_existe(item[2:]):
                    keys_args.append(item[2:])
                    # TODO adicionar validação com o template dos argumentos
                else:
                    sys.exit(
                        f'Erro: O argumento fornecido <{item}> não existe nos argumentos disponíveis'
                    )
            else:
                values_args.append(item)

        return dict(zip(keys_args, values_args))

    def args_list_pre_validation(self, args: list[str]) -> list[str]:
        # Ignora o primeiro elemento dos argumentos - o nome/path do ficheiro
        del args[0]

        # Verifica se existem argumentos, retorna "help" do script
        if args.__len__() < 3:
            # Temporário
            sys.exit(
                'O programa deve ser chamado com pelo menos 1 argumento e valor')

        # Verifica argumentos sem valor, mas defenidos
        if args.__len__() % 2 != 0:
            sys.exit(
                'Erro: Todos os argumentos chamados devem ter valores associados')

        return args

    def arg_existe(self, arg: str) -> bool:
        """Verifica se o argumento dado existe na lista de argumentos possiveis

        Args:
            arg (str): O argumento a verificar se a existencia é válida

        Returns:
            bool: Se existir retorna True, se não False
        """
        return self.argumentos.keys().__contains__(arg)
