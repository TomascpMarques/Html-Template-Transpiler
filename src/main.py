"""
O ponto inicial do programa
"""

import sys
import re


def main():
    """
    Função a correr se o ficheiro
    for invocado como um script
    """
    some = parse_cmd_args(sys.argv)
    print(some)


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


if __name__ == '__main__':
    main()
