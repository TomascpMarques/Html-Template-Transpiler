"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""


from dataclasses import dataclass
import os
from typing import Any, Callable
from cli.erros import erro_exit

from file_handeling.handler import FileHandler, parse_htt_file
from file_templating.template_conf import TemplateConfig


@dataclass()
class TemplateFile:
    """
    Some Some
    """

    def __init__(self, file_tags: dict[str, list[str]]):
        # adiciona os valores passados de file_tags
        # para atributuos da class
        for chave, valor in file_tags.items():
            self.__setattr__(chave, valor)

        self.validar_keys_template()

    def __getattr__(self, key: str):
        return self.__dict__[key]

    def items(self) -> tuple:
        """
        Devolve os atributuos da class numa tuple

        Returns:
            tuple: Um par com um dos atributuos da class
        """
        for key, val in self.__dict__.items():
            yield (key, val)

    def get(self, key: str) -> Any:
        """
        Devolve o atributuo pedido, através de uma key

        Args:
            key (str): Key do atributuo a devolver

        Returns:
            any: Valor de retorno
        """
        return self.__getattr__(key)

    def keys(self) -> list[str]:
        """
        Retorna as keys/valores da class

        Returns:
            list[str]: Lista dos valores existentes da class
        """
        return list(
            map(
                lambda x: x.replace('__', ''),
                self.__dict__
            )
        )

    def keys_por_tipo(self, tipo: str) -> list[str]:
        """
        Devolve todas as keys semelhantes ao tipo especificado

        Args:
            tipo (str): Tipo da key a agrupar

        Returns:
            list[str]: Lista das keys semelhantes ao tipo dado
        """
        return list(
            key for key in self.keys() if key.endswith(tipo)
        )

    def validar_keys_template(self) -> None:
        """
        Verifica se as keys fornecidas pelo template contêm a informação base necessária
        """
        valid_keys: list[str] = ['tag', 'conteudo']
        for section in self.keys():
            section_keys = self.get(section).keys()
            if set(valid_keys) != set(section_keys):
                error_mss = \
                    f'A secção <{section}>, contêm valores inválidos.\
                    \nEsperados: <{valid_keys}>\nDados:     <{list(section_keys)}>'

                erro_exit(
                    menssagen=error_mss,
                    time_stamp=True,
                    tipo_erro='BadSectionOptVals'
                )


@dataclass()
class TemplatingFiles(FileHandler):
    """
    Gestão e utilização dos ficheiros htt, tanto de config como os de templating
    """

    def __init__(self, path: str, configs: TemplateConfig):
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        # Conteudo existente no path especifico
        self.conteudo_dir: dict[str, os.DirEntry] = \
            super().conteudo_dir_entrys()

        # Leitura e atribuição dos ficheiros de templating htt
        self.htt_templates: dict[str, TemplateFile] = {}
        self.resolve_htt_templates()

        HTMLGenerator(
            htt_templates=self.htt_templates,
            file_handeling=self,
            configs=configs
        )

    def resolve_htt_templates(self) -> None:
        """
        Resolve os ficheiros htt e retira a informação inerente aos mesmos
        """
        for chave, dir_entry in self.conteudo_dir.items():
            # só lê o ficheiro se não for um file de config e não uma pasta
            if '.httconfig' not in chave and dir_entry.is_file():
                self.htt_templates.setdefault(
                    chave,
                    # Criação do TemplateFile através da info. dada
                    TemplateFile(
                        # Análise do ficheiro e parse do mesmo
                        parse_htt_file(
                            # leitura do conteudo do ficheiro no disco
                            super().
                            resolver_conteudo_ficheiro(dir_entry.path)
                        )
                    ),
                )


###############################################################################

class HTMLGeneratorTags:
    """
    AAAA
    """

    def __init__(self) -> None:
        self.funcs: dict[str, Callable] = dict(
            (func_name[:-4], self.__getattribute__(func_name))
            for func_name in self.__dir__() if '_tag' in func_name
        )

    @staticmethod
    def h1_tag(conteudo: str, /, tag_id: str = '') -> str:
        """[summary]

        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return f'<h1 id="{tag_id.replace(" ","-")}">{conteudo}</h1>'


class HTMLGenerator(HTMLGeneratorTags):
    """
    Some
    """

    def __init__(
            self,
            htt_templates: dict[str, TemplateFile],
            file_handeling: FileHandler,
            configs: TemplateConfig
    ):
        super().__init__()

        self.templates: dict[str, TemplateFile] = htt_templates
        self.file_handeling: FileHandler = file_handeling
        self.configs: TemplateConfig = configs

        self.output_pasta_path: str = self.file_handeling.criar_pasta(
            'htt-oputut'
        )

        self.gen_html()

    def gen_html(self) -> None:
        """
        Generates HTML from the given htt template data
        """
        for template_file_name, template in self.templates.items():
            novo_conteudo_ficheiro: list[str] = []
            nome_ficheiro: str = template_file_name[
                :template_file_name.index('.')
            ]

            novo_ficheiro_path = self.file_handeling.criar_ficheiro(
                nome_ficheiro=nome_ficheiro,
                extensao='.html',
                path=self.output_pasta_path,
            )

            for section_name, section in template.items():
                novo_conteudo_ficheiro.append(
                    self.funcs[section.get('tag')](
                        section.get('conteudo'),
                        tag_id=section_name
                    )
                )

            self.file_handeling.escrever_conteudo_ficheiro(
                conteudo=novo_conteudo_ficheiro,
                ficheiro=novo_ficheiro_path,
                modo='a'
            )
