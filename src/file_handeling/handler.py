"""
Lida com ficheiros e as suas pastas
"""

# """
# Estrutura:
#     /pasta
#     |_ .httconfig
#     |_ file1.htt
#     |_ file2.htt
#     |_ /pasta_2
#         |_ file3.htt
# """


import os
import sys

from cli.erros import erro_exit


FILE_EXTENSIONS: list[str] = ['.htt', '.httconfig']


class FileHandler:
    """
    Esta classe gere a utilização de ficheiros e pastas de acordo com as necessidades
    do programa
    """

    def __init__(self, path: str):
        self.caminho: str = path

        # Normalização do camiho do file handler atual
        os.chdir(self.caminho)

        # Procura por ficheiros e pastas que possam conter ficheiros válidos
        self.ficheiros: dict[str, os.DirEntry] = dict(
            (entrada.name, entrada) for entrada in os.scandir(path)
            if (
                entrada.is_file()
                and entrada.name[entrada.name.index('.'):]
                in FILE_EXTENSIONS
            ) or entrada.is_dir()
        )

        # Verifica se a pasta alvo contêm o conteudo minímo necessário
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

    def resolver_conteudo_ficheiro(self, path: str) -> str:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            caminho (str): Path do ficheiro a ler o conteudo

        Returns:
            list[str]: Conteudos do ficheiro em linhas
        """
        print(f'{self.ficheiros.get(path).path}')
        with open(
            os.path.join(self.caminho, path),
            'r', encoding=sys.getfilesystemencoding()
        ) as ficheiro:
            return ficheiro.read()

    def ficheiro_dir_entry(self, path: str) -> os.DirEntry | None:
        """
        Devolve a dir entry do ficheiro pedidos

        Returns:
            os.DirEntry | None: A dir entry especificada ou None
        """
        if path not in self.ficheiros.keys():
            return None
        return self.ficheiros.get(path)

    def ficheiros_dir_entrys(self, *caminhos: str) -> list[os.DirEntry]:
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

    def resolver_conteudo_ficheiros(self, *caminhos: str) -> str:
        """
        Devolve o conteudo dos ficheiros pedidos

        Args:
            nomes (list[str]): nomes dos ficheiros a fazer dump

        Returns:
            list[list[str]]: O conteudo dos ficheiros, separados por linhas
        """
        conteudo: str = ''
        for nome in caminhos:
            try:
                with open(
                    os.path.join(self.caminho, nome),
                    'r',
                    encoding=sys.getfilesystemencoding()
                ) as file:
                    conteudo = file.readlines()
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
        return conteudo

    def criar_ficheiro(self, nome_ficheiro: str, path: str = '', extensao: str = '.htt') -> None:
        """
        Cria um ficheiro a partir dos dados fornecidos

        Args:
            nome_ficheiro (str): Nome a dar ao novo ficheiro
            path (str): Path a usar para criar o ficheiro
            extensao (str): Extensão a colocar no ficheiro
        """
        with open(
                os.path.join(
                    self.caminho,
                    (path + nome_ficheiro + extensao)
                ),
                'w', encoding=sys.getfilesystemencoding()) as file:
            file.close()

    def escrever_conteudo_ficheiro(
            self,
            conteudo: str | list,
            # nome do ficheiro (str) ou estrutura da linguagem python
            ficheiro: os.DirEntry | str
    ) -> None:
        """
        Escreve o conteudo fornecido num ficheiro especificado

        Args:
            conteudo (str | list[str]): Conteudo a ser escrito no ficheiro fornecido
            ficheiro (os.DirEntry | str): Ficheiro alvo a ser escrito o conteudo, ou o nome do mesmo
        """

        # Avalia o type do ficheiro dado,
        # se for string, irá ser conssiderado como um nome de ficheiro,
        # e utilizado a partir do caminho defenido para o filehandler.
        #
        # Se for do tipo os.DirEntry, executa as operações de verificação
        # e uso do mesmo com os dados contido na estrutura
        if isinstance(ficheiro, os.DirEntry):
            if ficheiro.name not in self.nome_ficheiros():
                erro_exit(
                    menssagen='O ficheiro dado não existe',
                    time_stamp=True,
                    tipo_erro='FileNaoExiste'
                )
            else:
                pass
        elif isinstance(ficheiro, str):
            if ficheiro not in self.nome_ficheiros():
                erro_exit(
                    menssagen='O ficheiro dado não existe',
                    time_stamp=True,
                    tipo_erro='FileNaoExiste'
                )
            else:
                pass
        else:
            erro_exit(
                menssagen='Erro ao tentar processar o ficheiro pedido',
                time_stamp=True,
                tipo_erro='BadFileGiven'
            )

        # Verifica o tipo de conteudo e escreve o mesmo no ficheiro
        # para a execução do programa se o conteudo for inváilido
        with open(
            os.path.join(self.caminho, ficheiro),
            'w', encoding=sys.getfilesystemencoding()
        ) as file:
            if isinstance(conteudo, str):
                file.write(conteudo)
            elif isinstance(conteudo, list):
                file.writelines(
                    map(
                        lambda x: x + '\n',
                        conteudo
                    )
                )
            else:
                file.close()
                erro_exit(
                    menssagen='O tipo de conteudo fornecido não é valido para a operação a efetuar',
                    time_stamp=True,
                    tipo_erro='BadContentGiven'
                )
