"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""
# Other imports
import asyncio
import os
from dataclasses import dataclass
from typing import Any

# Program Modules
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
        valid_keys: list[str] = ['tag']
        for section in self.keys():
            section_keys = self.get(section).keys()
            if not set(valid_keys).issubset(set(section_keys)):
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
        asyncio.run(
            self.resolve_htt_templates()
        )

        HTMLGenerator(
            htt_templates=self.htt_templates,
            file_handeling=self,
            configs=configs
        )

    async def resolve_htt_templates(self) -> None:
        """
        Resolve os ficheiros htt e retira a informação inerente aos mesmos
        """
        for chave, dir_entry in self.conteudo_dir.items():
            # só lê o ficheiro se não for um file de config e não uma pasta
            if '.httconfig' not in chave and dir_entry.is_file():
                # Async set new htt template in, self.htt_templates
                await asyncio.get_running_loop().create_task(
                    asyncio.to_thread(
                        self.htt_templates.setdefault,
                        chave,
                        TemplateFile(
                            # Análise do ficheiro e parse do mesmo
                            parse_htt_file(
                                # leitura do conteudo do ficheiro no disco
                                self.resolver_conteudo_dir_entry(dir_entry)
                            )
                        ),

                    )
                )

##############################################################################


class HTMLGeneratorTags:
    """
    Gera tags de HTML
    """

    def __init__(self) -> None:
        # Adiciona as funcs disponiveis para gerar tags de html
        # através dos atributuos registados na class
        self.valid_tags: list[str] = [
            'h1', 'h2', 'h3',
            'h4', 'h5', 'p',
            'span', 'hr', 'a'
        ]

    @staticmethod
    def tag_builder(
        h_tag: str,
        conteudo: str,
        /,
        other_options: dict[str, str],
        tag_id: str = ''
    ) -> str:
        """
        Builds html h<n> tags
        """

        html_tag_options: list[tuple[str, str]] = []
        if other_options is not None:
            for key, val in other_options.items():
                if key not in ['tag', 'conteudo']:
                    html_tag_options.append((key, val))

        print(f'{html_tag_options=}')

        use_html_options: str = ''
        if html_tag_options is not None:
            for opt, vals in html_tag_options:
                use_html_options += (f'{opt}="{vals}" ')

        conteudo_not_none: str = conteudo if conteudo is not None else ''
        id_tag: str = tag_id.replace(" ", "-")

        return f'<{h_tag} id="{id_tag}"{use_html_options}>{conteudo_not_none}</{h_tag}>'

    def html_tag_resolve(
        self,
        /, other_options: dict[str, str],
        tag: str = '',
        tag_id: str = ''
    ) -> str:
        """
        Resolve as tags fornecidas pelo programa, para html válido
        """
        if tag not in self.valid_tags:
            erro_exit(
                menssagen=f'A tag fornecida não é válida <{tag}>',
                time_stamp=True,
                tipo_erro='BadTagGiven'
            )
            return ''

        if other_options.get('conteudo') is None:
            return self.tag_builder(
                tag,
                '',
                tag_id=tag_id,
                other_options=other_options
            )

        return self.tag_builder(
            tag,
            other_options['conteudo'],
            tag_id=tag_id,
            other_options=other_options
        )


class HTMLGenerator(HTMLGeneratorTags):
    """
    Reads template file content and generates HTML from it.
    """

    def __init__(
            self,
            htt_templates: dict[str, TemplateFile],
            file_handeling: FileHandler,
            configs: TemplateConfig
    ):
        # Setup of html tag generator
        super().__init__()

        # htt templates
        self.templates: dict[str, TemplateFile] = htt_templates

        # Needed Templater functionalitty
        self.file_handeling: FileHandler = file_handeling
        self.configs: TemplateConfig = configs

        # End result folder
        self.output_pasta_path: str = self.file_handeling.criar_pasta(
            'htt-oputut'
        )

        # Corre de uma maneira asyncrona e threaded
        asyncio.run(
            self.gen_html()
        )

    @staticmethod
    def _setup_css_fontes(fontes_escolhidas: list[str]) -> str:
        fonts_css_import: str = "\t@import url('https://fonts.googleapis.com/css2?"

        # Se não for escolhida nenhuma fonte, devolve uma str vazia.
        # O setup do css lida com o facto de não se escolher nehuma fonte,
        # atribui a fonte 'Arial' a todas as tags
        if fontes_escolhidas.__len__() < 1:
            return ''

        # Initial font setup
        fonts_css_import += 'family=' + fontes_escolhidas[0]

        # Itera sobre todas as fontes menos a já adicionada
        for font in fontes_escolhidas[1:]:
            fonts_css_import += '&family=' + font

        # Termina a string de import das fontes e devolve a mesma
        return fonts_css_import + "');"

    def _setup_fonts_for_spef_tags(self) -> str:
        fonts_for_tags: str = '\n'.join(
            f"\n\t\t{tag} {{font-family: '{font}', sans-serif;}}"
            for tag, font in
            self.configs.fontes.items()
        )
        return fonts_for_tags

    def _setup_htt_css(self) -> str:
        """
        Setup do css defenido no template, a usar pelos ficheiros html
        """
        fonts_normalizadas_para_import: list[str] = list(
            font.replace(' ', '+')
            for _, font in self.configs.fontes.items()
        )

        # html file css setup, for fonts and tag specific fonts
        setup_htt_css: list[str] = [
            '\t<style type="text/css">\n',
            (
                '\t'
                + self._setup_css_fontes(fonts_normalizadas_para_import)
                + '\n'
            ),
            (
                '\t'
                + self._setup_fonts_for_spef_tags()
                + '\n'
            ),
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
            self._setup_htt_css(),
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
                    # cicle
                    self.html_tag_resolve(
                        other_options=section,
                        tag=section['tag'],
                        tag_id=section_name,
                    )
                )
            except KeyError as err:
                erro_exit(
                    menssagen=f'O valor <{err}>, não foi fornecido',
                    tipo_erro='NotEnoughVals',
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

    def insert_css_style(self) -> None:
        """
        Copia o ficheiro de estilo defenido através
        da opção "tema" no ficheiro .htt-config,
        para a pasta de output "htt-output"
        """

        # Get css theme file path
        tema_css_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'css',
            (self.configs.tema + '.css')
        )

        # Write css file to htt-output
        self.file_handeling.escrever_conteudo_ficheiro(
            ficheiro=os.path.join(
                self.output_pasta_path,
                (self.configs.tema + '.css')
            ),
            modo='w',
            conteudo=self.file_handeling.resolver_conteudo_ficheiro(
                tema_css_path
            )
        )

    async def gen_html(self) -> None:
        """
        'Transpila' os conteudos dos templates htt, para html e css
        de uma maneira asyncrona e threaded
        """
        # Ao utilizar o loop das running tasks, posso adicionar tasks ao mesmo loop,
        # sem bloquear o loop que itera pelos templates, e o loop das tasks

        # Get templates to transpile
        for template_name, template_file in self.templates.items():
            # Get the running tasks @ loop
            asyncio.get_running_loop().\
                create_task(  # Create a new task for a new file
                    # And make that task run on a new thread
                    asyncio.to_thread(
                        self.transpile_htt_to_html,
                        template_name,
                        template_file
                    )
            )

        # Add css style
        self.insert_css_style()
