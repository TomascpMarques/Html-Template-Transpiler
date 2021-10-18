"""
Modulo relativo à interação do user com o programa através do terminal
"""

import sys
import re
from dataclasses import dataclass, field

from cmd_module.cmd_args import CmdArgumento, validar_argumento, CMD_ARGS


class Cmd:
    """
    Propiedades da cmd/interação do user com a aplicação,
    contêm os argumentos disponiveis, e valida e interage
    com os pedidos do utilizador
    """

    def __init__(self, **kwargs: CmdArgumento):
        self.argumentos: dict[str, CmdArgumento] = dict(
            (key, kwargs[key]) for key in kwargs
        )

    def parse_cmd_args(self, args: 'list[str]'):
        """Parse os argurmentos dados ao correr o script

        Args:
            args(list[str]): Os argumentos usados ao correr o script

        Returns:
            dict: Os argumentos usados em formato de dicionario
        """

        # pre validação dos argumentos dados
        self.arg_list_pre_validacao(args)

        # retira as keys dos argumentos
        keys_args: list[str] = []
        values_args: list[str] = []

        for item in args:
            if re.compile(r'--\w+').match(item) is not None:
                # item[2:] -> Ignora os simbolos pre chave ex: "(--)chave"
                # Verifica se o argumento fornecido pelo user existe
                if self.arg_existe(item[2:]):
                    keys_args.append(item[2:])
                else:
                    # Se não existir o programa para, e devolve um erro
                    sys.exit(
                        f'Erro: O argumento fornecido <{item}> não existe nos argumentos disponíveis'
                    )
            else:
                values_args.append(item)

        # Atualizar o campo "argumentos" com o dicionario dos argumentos/valores extraidos
        self.argumentos = dict(zip(keys_args, values_args))

        # Valida os argumentos extraidos
        for arg in self.argumentos:
            sys.exit(f'{CMD_ARGS[arg].erro_validacao}') if not validar_argumento(
                CMD_ARGS[arg], self.argumentos[arg]) else None

    def arg_list_pre_validacao(self, args: list[str]) -> list[str]:
        # Ignora o primeiro elemento dos argumentos - o nome/path do ficheiro
        del args[0]

        # Verifica se existem argumentos, retorna "help" do script
        if args.__len__() < 2:
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
