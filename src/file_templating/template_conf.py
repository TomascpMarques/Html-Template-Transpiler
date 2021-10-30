"""
Configurações do templating
"""

import re


class Configs:
    """
    Gere e armazena as configurações para o templating
    do site a gerar
    """

    def __init__(self, conteudo: str):
        # Configs Esperadas
        self.fontes: dict[str, str] = {}
        self.tema: str = ''
        self.estilo: str = ''
        # End Configs Esperadas

        self.parse_config(conteudo_ficheiro=conteudo)
        for some in self.valores_config():
            print(f'{self.__getattribute__(some)=}, {some=}')

    def valores_config(self) -> list[str]:
        """
        Retorna os valores de config existentes na class

        Returns:
            list[str]: Valores disponiveis
        """
        return list(
            map(
                lambda x: x.replace('__', ''),
                self.__dict__
            )
        )

    def parse_config(self, conteudo_ficheiro: str) -> None:
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

        # Esta lista vai guardar os valores em que
        # os caracteres desnecessários são retirados
        lista_temp_valores_conf: list[str] = []
        for word in conteudo_ficheiro:
            for char in ['    ', '\t', '\n']:
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
            if '>' in valor and ',' in valor:
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
            if '.' in valor:
                return float(valor)

            # default catch
            return valor

        # Cria o dicionário com os valores e chaves corretos
        # de config, para adicionar à struct
        configs_valores_dict: dict[str, list[str]] = dict(
            (
                line[0: line.index(':')-1],   # key
                formatar_valor(
                    line[line.index(':')+1:]  # valor
                )
            ) for line in lista_temp_valores_conf
        )

        #  Adiciona os valores e atributuos corretos à class
        for chave, valor in configs_valores_dict.items():
            self.__setattr__(chave, valor)


class TemplateConfig:
    """
    Some Some
    """

    def __init__(self, conf_file: str):
        self.conf: Configs = Configs(conf_file)
