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
import re

from cli.erros import erro_exit


HTT_FILE_EXTENSIONS: list[str] = ['.htt', '.httconfig']


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
        self._conteudo: dict[str, os.DirEntry] = dict(
            (entrada.name, entrada) for entrada in os.scandir(path)
            if (
                entrada.is_file()
                and entrada.name[entrada.name.index('.'):]
                in HTT_FILE_EXTENSIONS
            ) or entrada.is_dir()
        )

        # Verifica se a pasta alvo contêm o conteudo minímo necessário
        if not self._conteudo.__len__():
            erro_exit(
                menssagen='A pasta têm de ter no minimo um ficheiro de configuração',
                time_stamp=True,
                tipo_erro='NotEnoughFiles'
            )

    def conteudo_dir_entrys(self) -> dict[str, os.DirEntry]:
        """
        Devolve as direntrys dos ficheiros e pastas encontradas

        Returns:
            dict[str, os.DirEntry]: Conteudo encontrado no path inicial especificado
        """
        return self._conteudo.copy()

    def nome_ficheiros(self) -> list[str]:
        """
        Devolve os nomes dos ficheiros existentes

        Returns:
            list[str]: [description]
        """
        return self._conteudo.keys()

    @staticmethod
    def resolver_conteudo_ficheiro(path: str) -> str:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            caminho (str): Path do ficheiro a ler o conteudo

        Returns:
            list[str]: Conteudos do ficheiro em linhas
        """
        with open(
            path, 'r',
            encoding=sys.getfilesystemencoding()
        ) as ficheiro:
            return ficheiro.read()

    def resolver_conteudo_dir_entry(self, dir_entry: os.DirEntry) -> str:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            file_entry (os.DirEntry): A dir entry do ficheiro a ler o conteudo

        Returns:
            str: Conteudo do ficheiro
        """
        return self.resolver_conteudo_ficheiro(dir_entry.path)

    def path_get_dir_entry(self, path: str) -> os.DirEntry | None:
        """
        Devolve a dir entry do ficheiro pedido

        Returns:
            os.DirEntry | None: A dir entry especificada ou None
        """
        if path not in self._conteudo.keys():
            return None
        return self._conteudo.get(path)

    def get_current_dir_entrys(self) -> list[os.DirEntry]:
        """
        Devolve as dir entrys do path atual

        Returns:
            list[os.DirEntry]: Dir entrys no path
        """
        return list(entry for _, entry in self._conteudo.items() if entry.is_file())

    def path_get_dir_entrys(self) -> list[os.DirEntry]:
        """
        Devolve as dir entrys dos ficheiro pedidos

        Returns:
            list[os.DirEntry]: Lista das dir entries dso ficheiros pedidos
        """
        return self.get_current_dir_entrys()

    def dir_entrys_por_extensao(self, extensao: str) -> list[os.DirEntry]:
        """
        Devolve todas as dir entrys em que a extensão de ficheiro é equivalente à pedida
        no path (caminho) fornecido

        Returns:
            list[os.DirEntry]: Dir entrys com a extensão de ficheiro pedida
        """
        return list(
            filter(
                lambda x: x.name[x.name.index('.'):] == extensao,
                self.get_current_dir_entrys()
            )
        )

    @staticmethod
    def resolver_conteudo_ficheiros(*caminhos: str) -> str:
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
                    nome,
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

    @staticmethod
    def criar_pasta(path: str) -> str:
        """
        Cria uma pasta para o output do programa
        """
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        return path

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
            ficheiro,
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


def parse_htt_file(conteudo_ficheiro: str) -> dict[str, dict[str, any]]:
    """
        Retira os valores de config existentes no ficheiro ".httconfig"
        do projeto e adiciona esses mesmos valores à class

        Args:
            conteudo_ficheiro (str): Conteudo do ficheiro de config
        """

    # Divide o conteudo do ficheiro através de new-lines vazias
    # Ex:
    #     fontes :
    #         sdasdas,
    #         asdasd,
    #     <empty new line>
    #     some :
    #         some
    conteudo_ficheiro = \
        re.split(
            re.compile(r"^\n", re.MULTILINE),
            conteudo_ficheiro
        )

    # Esta lista vai  guardar os valores em que
    # os caracteres desnecessários são retirados
    lista_temp_valores_conf: list[str] = []
    for word in conteudo_ficheiro:
        for char in ['    ', '\t', '\n', '\t ']:
            word = word.replace(char, '')
        lista_temp_valores_conf.append(word)

       # Formata os valores de acordo com a sua estrutura em python
    def formatar_valor(valor: str) -> list[str] | int | float:
        """
        De acordo com a estrutura do valor,
        devolve uma estrutura equivalente em python

        Args:
            valor (str): Valor a formatar

        Returns:
            list[str] | int | float: Valor corretamente formatado
        """
        # print(f'{valor=}')
        # print(f'{list(map(lambda x: x.split(" > "),valor.split(",")))=}')
        if '>' in valor:
            # dict de valores
            return dict(
                # a func map acaba por dividir o conteudo
                # em listas de strings de 2 valores cada,
                # o que permite transformar essas listas em Dicts
                map(
                    lambda x: x.split(' > '),
                    valor.split(',')
                )
            )
        if ',' in valor:
            # lista de strings
            return valor.split(',')
        if valor.isnumeric():
            return int(valor)
        if re.match(r'\d+', valor):
            return float(valor)

        # default catch
        return valor

       # Cria o dicionário com os valores e chaves corretos
       # de config, para adicionar à struct
    configs_valores_dict: dict[str, dict[str, any]] = dict(
        (
            line[0: line.index(':')-1],   # key
            formatar_valor(
                line[line.index(':')+1:]  # valor
            )
        ) for line in lista_temp_valores_conf
    )

    return configs_valores_dict
