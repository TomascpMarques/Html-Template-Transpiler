"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Callable

from cli.erros import erro_exit
from file_handeling.handler import FileHandler, parse_htt_file
from file_templating.template_conf import TemplateConfig


@dataclass()
class TemplateFile():
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
        return self.__dict__.get(key)

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
            if not set(section_keys).issubset(set(valid_keys)):
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
    def tag_builder(h_tag: str, conteudo: str, /, tag_id: str = '') -> str:
        """
        Builds html h<n> tags
        """
        return f'<{h_tag} id="{tag_id.replace(" ","-")}">{conteudo}</{h_tag}>'

    def h1_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('h1', conteudo, tag_id=tag_id)

    def h2_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('h2', conteudo, tag_id=tag_id)

    def h3_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('h3', conteudo, tag_id=tag_id)

    def h4_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('h4', conteudo, tag_id=tag_id)

    def h5_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('h5', conteudo, tag_id=tag_id)

    def span_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('span', conteudo, tag_id=tag_id)

    def p_tag(self, conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('p', conteudo, tag_id=tag_id)

    def hr_tag(self, _conteudo: str, /, tag_id: str = '') -> str:
        """
        Args:
            conteudo (str): [description]
            id (str, optional): [description]. Defaults to ''.

        Returns:
            str: [description]
        """
        return self.tag_builder('hr', '', tag_id=tag_id)


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

        asyncio.run(
            self.gen_html()
        )

    def setup_htt_css(self) -> str:
        """
        Setup do css defenido no template, a usar pelos ficheiros html
        """
        fonts_parse: list[str] = list(
            font.replace(' ', '+') for _, font in self.configs.fontes.items()
        )

        fonts: str = "\t@import url('https://fonts.googleapis.com/css2?"
        fonts += 'family=' + fonts_parse[0]
        for font in fonts_parse[1:]:
            fonts += '&family=' + font
        fonts += "');"

        fonts_for_tags: str = '\n'.join(
            f"\n\t\t{tag} {{font-family: '{font}', sans-serif;}}"
            for tag, font in self.configs.fontes.items()
        )

        setup_htt_css: list[str] = [
            '\t<style type="text/css">\n',
            '\t' + fonts + '\n',
            '\t' + fonts_for_tags + '\n',
            '\t</style>'
        ]

        return ''.join(setup_htt_css)

    def gen_html_headers(self, pag_titulo: str, ficheiro_path: str | os.DirEntry) -> None:
        """
        Escreve os cabeçalhos html corretos no ficheiro
        """
        conteudo: list[str] = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '\t<meta charset="UTF-8">',
            '\t<meta http-equiv="X-UA-Compatible" content="IE=edge">',
            '\t<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'\t<title>{pag_titulo}</title>',
            f'\t<link rel="stylesheet" href="{self.configs.tema}.css">',
            self.setup_htt_css(),
            '</head>\n',
        ]

        # Escreve o conteudo html no ficheiro
        self.file_handeling.escrever_conteudo_ficheiro(
            conteudo=conteudo,
            ficheiro=ficheiro_path,
            modo='a+'
        )

    def transpile_htt_to_html(self, template_file_name: str, template: TemplateFile):
        """
        Asynchronously translate the htt file contents and write them to the html file
        """

        novo_conteudo_ficheiro: list[str] = []
        nome_ficheiro: str = template_file_name[
            :template_file_name.index('.')
        ]

        # Cria o novo ficheiro html
        ficheiro_path = self.file_handeling.criar_ficheiro(
            nome_ficheiro=nome_ficheiro,
            extensao='.html',
            path=self.output_pasta_path,
        )

        self.gen_html_headers(
            nome_ficheiro.capitalize(),
            ficheiro_path=ficheiro_path
        )

        novo_conteudo_ficheiro.append('<body>\n<main>')

        # Itera sobre as secções no template
        for section_name, section in template.items():
            # Adiciona ao novo conteudo para o ficheiro html
            try:
                novo_conteudo_ficheiro.append(
                    # Chama as funções adequadas para as tags dadas
                    self.funcs[section.get('tag')](
                        section.get('conteudo'),
                        tag_id=section_name
                    )
                )
            except KeyError:
                erro_exit(
                    menssagen=f'Valor <{section.get("tag")}> não está implementado para tags',
                    tipo_erro='FuncNotImplemented',
                    time_stamp=True
                )

        # Close html body
        novo_conteudo_ficheiro.append('</main></body>')
        # Close html tag
        novo_conteudo_ficheiro.append('\n</html>')

        # Escreve o conteudo html no ficheiro
        self.file_handeling.escrever_conteudo_ficheiro(
            conteudo=novo_conteudo_ficheiro,
            ficheiro=ficheiro_path,
            modo='a+'
        )

    async def gen_html(self) -> None:
        """
        Generates HTML from the given htt template data
        """

        # Get templates to transpile
        for template_name, template_file in self.templates.items():
            # Get the running tasks
            asyncio.get_running_loop().\
                create_task(  # Create a new task for a new file
                    # And make that task run on a new thread
                    asyncio.to_thread(
                        self.transpile_htt_to_html,
                        template_name,
                        template_file
                    )
            )

        # Copie the CSS file
        pat_to_css: str = self.file_handeling.criar_ficheiro(
            nome_ficheiro=self.configs.tema,
            extensao='.css',
            path=self.output_pasta_path
        )

        css_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'css',
            (self.configs.tema + '.css')
        )

        self.file_handeling.escrever_conteudo_ficheiro(
            ficheiro=pat_to_css,
            modo='a',
            conteudo=self.file_handeling.resolver_conteudo_ficheiro(
                css_dir
            )
        )
