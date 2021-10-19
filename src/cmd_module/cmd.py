"""
Modulo relativo à interação do user com o programa através do terminal
"""

import re

from cmd_module.cmd_args import CMD_ARGS
from cmd_module.cmd_arg_resolvers.cmd_arg_setup import CmdArgumento, validar_argumento
from cmd_module.cmd_erros import erro_exit


class CmdListner:
    """
    Propiedades da cmd/interação do user com a aplicação,
    contêm os argumentos disponiveis, e valida e interage
    com os pedidos do utilizador
    """

    def __init__(self, **kwargs: CmdArgumento):
        self.argumentos: dict[str, CmdArgumento] = dict(
            (key, val) for (key, val) in kwargs.items()
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

        # Atualizar o campo "argumentos" com o dicionario dos argumentos/valores extraidos
        self.argumentos = self.args_extrair_keys_and_vals(args)

        # Valida os argumentos extraidos
        for arg in self.argumentos:
            if not validar_argumento(
                CMD_ARGS[arg],
                self.argumentos[arg]
            ):
                erro_exit(
                    menssagen=f'{CMD_ARGS[arg].erro_validacao}',
                    time_stamp=True,
                    tipo_erro='Erro_Arg_Validacao'
                )
            else:
                pass

    def args_extrair_keys_and_vals(self, args: list[str]) -> dict[str, str]:
        """Extrai todos os argumentos e valores passados pelo user, e transforma os num novo dict do

        Args:
            args (list[str]): Lista de argumentos e valores a usar

        Returns:
            dict[str, str]: Os argumentos tratados e separados uns dos outros
        """
        keys_args: list[str] = []
        values_args: list[str] = []

        # retira as keys dos argumentos
        for item in args:
            if re.compile(r'--\w+').match(item) is not None:
                # item[2:] -> Ignora os simbolos pre chave ex: "(--)chave"
                # Verifica se o argumento fornecido pelo user existe
                if self.arg_existe(item[2:]):
                    keys_args.append(item[2:])
                else:
                    # Se não existir o programa para, e devolve um erro
                    erro_exit(
                        tipo_erro='Erro_Arg_Fornecido',
                        time_stamp=True,
                        menssagen=f'O argumento, <{item}> não existe nos argumentos disponíveis',
                    )
            else:
                values_args.append(item)

        # retorna o dicionario dos argumentos/valores extraidos
        return dict(zip(keys_args, values_args))

    def arg_list_pre_validacao(self, args: list[str]) -> list[str]:
        """Pre valida a lista de argumentos

        Args:
            args (list[str]): Lista de argumentos a validar

        Returns:
            list[str]: Lista de argumentos a tratada e validada
        """
        # Ignora o primeiro elemento dos argumentos - o nome/path do ficheiro
        del args[0]

        # Verifica se existem argumentos, retorna "help" do script
        if args.__len__() < 2:
            erro_exit(
                time_stamp=True,
                tipo_erro='Erro_Num_Args',
                menssagen='O programa deve ser chamado com pelo menos 1 argumento e valor',
            )

        # Verifica argumentos sem valor, mas defenidos
        if args.__len__() % 2 != 0:
            erro_exit(
                tipo_erro='Erro_Arg_Valrs',
                time_stamp=True,
                menssagen='Todos os argumentos chamados devem ter valores associados',
            )

        return args

    def arg_existe(self, arg: str) -> bool:
        """Verifica se o argumento dado existe na lista de argumentos possiveis

        Args:
            arg (str): O argumento a verificar se a existencia é válida

        Returns:
            bool: Se existir retorna True, se não False
        """
        return self.argumentos.keys().__contains__(arg)
