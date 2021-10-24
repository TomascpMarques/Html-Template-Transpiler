"""
Lida com ficheiros e as suas pastas
"""

# """
# Estrutura:
#     /pasta
#     |_ .httconfig
#     |_ file1.htt
#     |_ file2.htt
# """


import os
import sys

from cli.erros import erro_exit


FILE_EXTENSIONS: list[str] = [r'.htt', r'.httconfig']


class FileHandler:
    """
    Handles file rading/writting
    """

    def __init__(self, caminho: str):
        self.ficheiros: dict[str, os.DirEntry] = dict(
            (entrada.name, entrada) for entrada in os.scandir(caminho)
            if entrada.is_file()
            and entrada.name[entrada.name.index('.'):]
            in FILE_EXTENSIONS
        )

        if not self.ficheiros.__len__():
            erro_exit(
                menssagen='A pasta têm de ter no minimo um ficheiro de configuração',
                time_stamp=True,
                tipo_erro='NotEnoughFiles'
            )

        self.caminho: str = caminho
        print(self.ficheiros)

    def nome_ficheiros(self) -> list[str]:
        """
        Devolve os nomes dos ficheiros existentes

        Returns:
            list[str]: [description]
        """
        return self.ficheiros.keys()

    def resolver_ficheiro(self, nome: str) -> list[str]:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            nome (str): Nome do ficheiro a ler o conteudo do ficheiro

        Returns:
            list[str]: Conteudos do ficheiro em linhas
        """
        with open(
            os.path.join(self.caminho, nome),
            'r', encoding=sys.getdefaultencoding()
        ) as file:
            return list(map(lambda x: x.replace('\n', ''), file.readlines()))


# def buscar_configs(self):
#         """
#         Busca a os.DirEntry configs para o projeto e a sua transpilação

#         Returns:
#             os.DirEntry: O ficheiro com as configs em formato de estrutura
#         """
#         self.configs = self.ficheiros.get('.httconfig')
#         return self

#     def ler_configs(self) -> list[str]:
#         """
#         Lê as configs para o projeto e devolve o conteudo das mesmas

#         Returns:
#             list[str]: Conteudo das configs para o projeto
#         """
#         with open(self.configs.name, 'r', encoding=sys.getfilesystemencoding()) as file:
#             return file.readlines()
