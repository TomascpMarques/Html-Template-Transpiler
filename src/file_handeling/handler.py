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


FILE_EXTENSIONS: list[str] = ['.htt', '.httconfig']


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
            'r', encoding=sys.getfilesystemencoding()
        ) as ficheiro:
            return list(map(lambda x: x.replace('\n', ''), ficheiro.readlines()))

    def ficheiro_dir_entry(self, nome: str) -> os.DirEntry | None:
        """
        Devolve a dir entry do ficheiro pedidos

        Returns:
            os.DirEntry | None: A dir entry especificada ou None
        """
        if nome not in self.ficheiros.keys():
            return None
        return self.ficheiros.get(nome)

    def ficheiros_dir_entry(self, *nomes: str) -> list[os.DirEntry]:
        """
        Devolve as dir entrys dos ficheiro pedidos

        Returns:
            list[os.DirEntry]: Lista das dir entries dso ficheiros pedidos
        """
        lista_ficheiros: list[os.DirEntry] = []
        for nome in nomes:
            if nome not in self.ficheiros.keys():
                return []
            lista_ficheiros.append(self.ficheiros.get(nome))
        return lista_ficheiros

    def dump_ficheiros(self, nomes: list[str]) -> list[list[str]]:
        """
        Devolve o conteudo dos ficheiros pedidos

        Args:
            nomes (list[str]): nomes dos ficheiros a fazer dump

        Returns:
            list[list[str]]: O conteudo dos ficheiros, separados por linhas
        """
        lista_conteudo: list[list[str]] = [[]]
        for nome in nomes:
            with open(
                os.path.join(self.caminho, nome),
                'r', encoding=sys.getfilesystemencoding()
            ) as ficheiro:
                lista_conteudo.append(
                    [map(
                        lambda x: x.replace('\n', ''),
                        ficheiro.readlines()
                    )]
                )
        return lista_conteudo
