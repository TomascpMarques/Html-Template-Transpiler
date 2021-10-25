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
    Handles file rading/writting, também ficheiros dentro de pastas
    """

    def __init__(self, caminho: str):
        self.caminho: str = caminho

        self.ficheiros: dict[str, os.DirEntry] = dict(
            (entrada.name, entrada) for entrada in os.scandir(caminho)
            if (
                entrada.is_file()
                and entrada.name[entrada.name.index('.'):]
                in FILE_EXTENSIONS
            ) or entrada.is_dir()
        )

        for _, entry in self.ficheiros.items():
            print(f'{entry.path}')

        if not self.ficheiros.__len__():
            erro_exit(
                menssagen='A pasta têm de ter no minimo um ficheiro de configuração',
                time_stamp=True,
                tipo_erro='NotEnoughFiles'
            )

        print(self.ficheiros)

    def nome_ficheiros(self) -> list[str]:
        """
        Devolve os nomes dos ficheiros existentes

        Returns:
            list[str]: [description]
        """
        return self.ficheiros.keys()

    def resolver_ficheiro(self, caminho: str) -> list[str]:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            caminho (str): Path do ficheiro a ler o conteudo

        Returns:
            list[str]: Conteudos do ficheiro em linhas
        """
        print(f'{self.ficheiros.get(caminho).path}')
        with open(
            os.path.join(self.caminho, caminho),
            'r', encoding=sys.getfilesystemencoding()
        ) as ficheiro:
            return list(map(lambda x: x.replace('\n', ''), ficheiro.readlines()))

    def ficheiro_dir_entry(self, caminho: str) -> os.DirEntry | None:
        """
        Devolve a dir entry do ficheiro pedidos

        Returns:
            os.DirEntry | None: A dir entry especificada ou None
        """
        if caminho not in self.ficheiros.keys():
            return None
        return self.ficheiros.get(caminho)

    def ficheiros_dir_entry(self, *caminhos: str) -> list[os.DirEntry]:
        """
        Devolve as dir entrys dos ficheiro pedidos

        Returns:
            list[os.DirEntry]: Lista das dir entries dso ficheiros pedidos
        """
        lista_ficheiros: list[os.DirEntry] = []
        for nome in caminhos:
            if nome not in self.ficheiros.keys():
                return []
            lista_ficheiros.append(self.ficheiros.get(nome))
        return lista_ficheiros

    def dump_ficheiros(self, *caminhos: str) -> list[list[str]]:
        """
        Devolve o conteudo dos ficheiros pedidos

        Args:
            nomes (list[str]): nomes dos ficheiros a fazer dump

        Returns:
            list[list[str]]: O conteudo dos ficheiros, separados por linhas
        """
        lista_conteudo: list[list[str]] = []
        for nome in caminhos:
            try:
                with open(
                    os.path.join(self.caminho, nome),
                    'r',
                    encoding=sys.getfilesystemencoding()
                ) as file:
                    lista_conteudo.append(
                        file.readlines()
                    )
            except FileNotFoundError:
                erro_exit(
                    time_stamp=True,
                    tipo_erro='FileNotFoundError',
                    menssagen=f'O ficheiro <{nome}> não existe'
                )
            except IsADirectoryError:
                erro_exit(
                    time_stamp=True,
                    tipo_erro='IsADirectoryError',
                    menssagen=f'O ficheiro <{nome}> é uma diretoria, não um ficheiro'
                )
        return lista_conteudo
