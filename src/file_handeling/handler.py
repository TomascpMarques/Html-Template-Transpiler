"""
Lida com ficheiros e as suas pastas
"""

# """
# Estrutura:
#     /pasta
#     |_ .httconfig
#     |_ file1.htt
#     |_ file2.htt
####### Ainda por implementar #######
#     |_ /pasta_2
#         |_ file3.htt
# """

# Other imports
import os
import sys
import re
from typing import Any, Generator

# Program Modules
from cli.erros import erro_exit
from cli_store.store import cli_store_get

# Extensões utilizadas pelo sistema de templating
HTT_FILE_EXTENSIONS: list[str] = ['.htt', '.httconfig', '.htt.custom']


class FileHandler:
    """
    A classe gere a utilização de ficheiros e pastas
    de acordo com as necessidades do programa,

    Permite resolver conteudo de ficheiro/s através de paths e os.DirEntrys.
    Escrever conteudo em ficheiros, ler ficheiros e criar tanto pastas como ficheiros.
    """

    def __init__(self, path: str):
        # Normalize path before new class instance is created
        # with the original path where the app is being called
        # makes relative paths work correctly
        os.chdir(
            str(cli_store_get('base_path'))
        )

        # Defenição do caminho a ser utlizado pelo handler durante a sua existência
        self.caminho: str = path

        # Normalização do camiho do file handler atual
        try:
            self.caminho = os.path.abspath(self.caminho)
            os.chdir(self.caminho)
        except FileNotFoundError:
            erro_exit(
                'Erro ao tentar basear o projeto, a partir do path especificado,\n' +
                '  o ficheiro ou pasta não foi encontrada'
            )

        # Procura por ficheiros e pastas que possam conter ficheiros válidos
        try:
            self._conteudo: dict[str, os.DirEntry] = dict(
                (entrada.name, entrada) for entrada in os.scandir(os.getcwd())
                if entrada.is_file()
                and entrada.name[entrada.name.index('.'):]
                in HTT_FILE_EXTENSIONS
            )
        except FileNotFoundError:
            erro_exit(
                f'A pasta especificada <{self.caminho}>,\
                    não foi encontrada ou não contêm ficheiros válidos'
            )

        # Verifica se a pasta alvo contêm o conteudo minímo necessário
        if not self._conteudo.__len__():
            erro_exit(
                menssagen='A pasta têm de ter no minimo um ficheiro de configuração',
                time_stamp=True,
                tipo_erro='NotEnoughFiles'
            )

    def folder_names_in_path(self, __path: str = '') -> Generator[str, None, None]:
        """
        Yields all the folder names in the path
        """
        if __path == '':
            __path = self.caminho
        for folder in os.scandir(__path):
            if folder.is_dir():
                yield folder.name

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
        return list(self._conteudo.keys())

    @staticmethod
    def resolver_conteudo_ficheiro(path: str) -> str:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            caminho (str): Path do ficheiro a ler o conteudo

        Returns:
            list[str]: Conteudos do ficheiro em linhas
        """
        try:
            with open(
                path, 'r',
                encoding=sys.getfilesystemencoding()
            ) as ficheiro:
                return ficheiro.read()
        except FileNotFoundError:
            erro_exit(
                menssagen=f'O caminho para o ficheiro <{path}> não é válido',
            )
            return ''

    def resolver_conteudo_dir_entry(self, dir_entry: os.DirEntry) -> str:
        """
        Devolve o conteudo do ficheiro pedido

        Args:
            file_entry (os.DirEntry): A dir entry do ficheiro a ler o conteudo

        Returns:
            str: Conteudo do ficheiro
        """
        return self.resolver_conteudo_ficheiro(dir_entry.path)

    def path_get_dir_entrys(self, path: str) -> os.DirEntry | None:
        """
        Devolve a dir entry do ficheiro pedido

        Returns:
            os.DirEntry | None: A dir entry especificada ou None
        """
        if path not in self._conteudo.keys():
            return None
        return self._conteudo.get(path)

    def path_dir_entries(self, path: str = '') -> dict[str, os.DirEntry] | None:
        """
        Devolve as dir entrys do path pedido, a partir do caminho

        Returns:
            dict[str, os.DirEntry] | None: Dir entrys existentes ou None
        """
        # If default path use self.caminho else use caminho + path
        try:
            return dict(
                (dir_entry.name, dir_entry) for dir_entry in os.scandir(
                    self.caminho
                )
            ) if path == '' else dict(
                (dir_entry.name, dir_entry) for dir_entry in os.scandir(
                    os.path.join(
                        self.caminho,
                        os.path.abspath(path)
                    )
                )
            )
        except FileNotFoundError as err:
            erro_exit(
                menssagen=f'Ficheiro não encontrado\n <{err}>'
            )
            return None

    def get_current_dir_entry(self) -> list[os.DirEntry]:
        """
        Devolve as dir entrys do path atual

        Returns:
            list[os.DirEntry]: Dir entrys no path
        """
        return list(entry for _, entry in self._conteudo.items() if entry.is_file())

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
                self.get_current_dir_entry()
            )
        )

    @staticmethod
    def resolver_conteudo_ficheiros(*caminhos: str) -> list[str]:
        """
        Devolve o conteudo dos ficheiros pedidos

        Args:
            nomes (list[str]): nomes dos ficheiros a fazer dump

        Returns:
            list[list[str]]: O conteudo dos ficheiros, separados por linhas
        """
        conteudo: list[str] = []
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

    def criar_ficheiro(self, nome_ficheiro: str, path: str = '', extensao: str = '.htt') -> str:
        """
        Cria um ficheiro a partir dos dados fornecidos

        Args:
            nome_ficheiro (str): Nome a dar ao novo ficheiro
            path (str): Path a usar para criar o ficheiro
            extensao (str): Extensão a colocar no ficheiro

        Returns:
            Devolve o path para o novo ficheiro
        """
        novo_nome_ficheiro: str = os.path.join(
            self.caminho,
            path,
            nome_ficheiro + extensao
        )
        with open(
                novo_nome_ficheiro,
                'w', encoding=sys.getfilesystemencoding()) as file:
            file.close()
        return novo_nome_ficheiro

    @staticmethod
    def criar_pasta(path: str) -> str:
        """
        Cria uma pasta para o output do programa
        """
        try:
            splited_path: list[str] = list(
                filter(
                    lambda x: x != '',
                    path.split(os.path.sep)
                )
            )
            for index, _ in enumerate(splited_path):
                os.mkdir(
                    f"{os.path.sep}"
                    .join(splited_path[:index+1])
                )
        except FileExistsError:
            pass

        return path

    @staticmethod
    def escrever_conteudo_ficheiro(
        conteudo: str | list,
        # nome do ficheiro (str) ou estrutura da linguagem python
        ficheiro: str | os.DirEntry,
        modo: str = 'w'
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
        if (
            not isinstance(ficheiro, os.DirEntry)
            or isinstance(ficheiro, str)
        ):
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
            modo,
            encoding=sys.getfilesystemencoding()
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


def parse_htt_file(conteudo: str) -> dict[str, Any]:
    """
    Retira os valores de config existentes no ficheiro dado
    e retorna os valores extraidos

    Returns:
        dict[str, Any]: Um dicionário com as tags/valores dentro do ficheiro

    Args:
        conteudo_ficheiro (str): Conteudo do ficheiro de config
    """

    # Divide o conteudo do ficheiro através de new-lines vazias
    # Ex:
    #     fontes :
    #         some > foo,
    #         emos > bar
    #     \n<empty new line>
    #     some :
    #         some
    conteudo_ficheiro: list[str] = re.split(
        re.compile(r"^\n", re.MULTILINE),
        conteudo
    )

    unwantted_chars = ['    ', '\t', '\n', '\t ']
    # Esta lista vai  guardar os valores em que
    # os caracteres desnecessários são retirados
    lista_temp_valores_conf: list[str] = []
    for word in conteudo_ficheiro:
        for char in unwantted_chars:
            word = word.replace(char, '')
        lista_temp_valores_conf.append(word)

    # Formata os valores de acordo com a sua estrutura em python
    def formatar_valor(valor: str) -> str | list[str] | int | float | dict[str, str]:
        """
        De acordo com o formato do valor,
        devolve um objeto equivalente em python

        Args:
            valor (str): Valor a formatar

        Returns:
            list[str] | int | float: Valor corretamente formatado
        """
        if '>' in valor:
            try:
                # dict de valores
                return dict(
                    # a func map acaba por dividir o conteudo
                    # em listas de strings de 2 valores cada,
                    # o que permite transformar essas listas em Dicts
                    map(
                        lambda x: x.split(' > '),
                        valor.split(':.')
                    )
                )
            except ValueError as e:
                print(f"Error: {e}")
                error_mss = \
                    f'Valor inválido encontrado ao processar as tags fornecidas.\nValor: "{valor}"'
                erro_exit(
                    menssagen=error_mss,
                    time_stamp=True,
                    tipo_erro='BadTagGiven'
                )
        if re.match(r'\S+\,', valor) is not None:
            # lista de strings
            return list(
                filter(
                    lambda x: x != '',
                    valor.split(',')
                )
            )
        if valor.isnumeric():
            return int(valor)
        if re.match(r'\d+', valor) is not None:
            return float(valor)

        # default catch
        return valor

       # Cria o dicionário com os valores e chaves corretos
       # de config, para adicionar à struct

    configs_valores_dict: dict[str, object] = {}
    try:
        configs_valores_dict = dict(
            (
                line[0: line.index(':')-1],   # key
                formatar_valor(
                    line[line.index(':')+1:]  # valor
                )
            ) for line in lista_temp_valores_conf
        )
    except ValueError:
        erro_exit(menssagen='O ficheiro de template foi mal formatado,\
            \n verifique o fim do ficheiro',
                  time_stamp=True, tipo_erro='BadFileGiven')

    return configs_valores_dict
