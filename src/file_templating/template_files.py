"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""
# Other imports
import asyncio
import os
import re
from dataclasses import dataclass
from typing import Any, Generator
import requests

# Program Modules
from cli.erros import erro_exit
from cli_store.store import cli_store_get, cli_store_set, CLI_STORE
from file_handeling.handler import (
    HTT_FILE_EXTENSIONS,
    FileHandler,
    parse_htt_file
)

from file_templating.template_conf import TemplateConfig


@dataclass()
class TemplateFile():
    """
    Some Some
    """

    def __init__(self, file_tags: dict[str, dict[str, Any]]):
        # adiciona os valores passados de file_tags
        # para atributuos da class
        for chave, valor in file_tags.items():
            self.__setattr__(chave, valor)

        self.validar_keys_template()

    def __getattr__(self, key: str):
        return self.__dict__.get(key)

    def items(self) -> Generator:
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
            self.conteudo_dir_entrys()

        self.htt_templates: dict[str, TemplateFile] = {}

        # Leitura e atribuição dos ficheiros de templating htt
        asyncio.run(
            self.resolve_htt_templates(),
        )

        # Start html generation
        HTMLGenerator(
            htt_templates=self.htt_templates,
            file_handeling=self,
            configs=configs,
            custom_tags=self.resolve_custom_htt_tag_templates(
                configs=configs
            )
        )

    def handle_htt_manifesto(self, manifesto: dict[str, Any]) -> str:
        """
            Validates the base keys and values of the manifesto file
            Errors out of the program if the file is invalid.

            Returns: The new value of the custom tag path
        """
        base_valid_keys: tuple[str, str] = ('base folder', 'tags')
        if not set(manifesto).issubset(set(base_valid_keys)):
            error_mss: str = \
                'As chaves defenidas no manifesto não contêm a info. necessária\n' + \
                f'Dadas: {set(manifesto)}\nEsperadas: {base_valid_keys}\n'
            erro_exit(
                tipo_erro='BadManifestoKeys',
                menssagen=error_mss
            )

        base_folder_regex: re.Pattern = \
            re.compile(
                r'(([A-z-_]+\/)+)'
            )

        base_folder_manifest_val: str = manifesto[base_valid_keys[0]]
        custom_tags_manifest_val: list[str] = manifesto[base_valid_keys[1]]

        if re.match(base_folder_regex, base_folder_manifest_val) is None:
            erro_exit(
                menssagen='O link fornecido para o base folder das tags não é válido',
                tipo_erro='BadBaseFolderTags'
            )

        base_tags_folder: str = base_folder_manifest_val

        # Create the folder for storing the tags that will be requested from github
        if base_tags_folder not in self.folder_names_in_path():
            self.criar_pasta(
                base_tags_folder
            )

        if custom_tags_manifest_val.__len__() < 1:
            erro_exit(
                menssagen='O valor fonecido para as tags não é válido',
                tipo_erro='TagsCustomFileNameInvalid'
            )

        custom_tags_responses: list[requests.Response] = list(
            requests.get(
                'https://raw.githubusercontent.com/' + base_tags_folder + custom_tag
            ) for custom_tag in custom_tags_manifest_val
        )

        for index, request in enumerate(custom_tags_responses):
            if request.status_code != 200:
                error_mss: str = \
                    'Ocorreu um erro ao pedir o ficheiro <' + \
                    custom_tags_manifest_val[index] + '>'

                erro_exit(
                    menssagen=str(error_mss),
                    tipo_erro='ErroRequestingFile'
                )
            elif request.text != '':
                self.escrever_conteudo_ficheiro(
                    ficheiro=(
                        base_tags_folder +
                        custom_tags_manifest_val[index]
                    ),
                    modo='w',
                    conteudo=request.text,
                )

        # returns new value for custom_tags_path
        return base_tags_folder

    def resolve_custom_htt_tag_templates(
        self,
        configs: TemplateConfig
    ) -> dict[str, tuple[str, ...]] | None:
        """
        Resolve os templates para as tags htt custom
        """
        custom_tags_path: str | None = configs.get_config_valor("tags_custom")
        if custom_tags_path is None:
            return custom_tags_path

        # Import custom tags from the web
        # if tags_custom attribute is set to be a link
        link_regex_pattern: re.Pattern = re.compile(
            r'(([A-z-_]+\/)+)manifesto\.htt'
        )

        if re.match(link_regex_pattern, custom_tags_path) is not None:
            # The htt manifesto is a file in a github project directory,
            # that stores the base folders link for the custom tags folder,
            # and a list of the tag folders to download from the custom tags folder
            htt_manifesto_request: requests.Response = \
                requests.get(
                    url='https://raw.githubusercontent.com/' + custom_tags_path
                )

            if (
                htt_manifesto_request.status_code != 200
                or htt_manifesto_request.text.__len__() <= 1
            ):
                erro_exit(
                    menssagen='O ficheiro de manifesto para as tags não foi alcançado',
                    tipo_erro='ManifestoNotUsable'
                )
                return None

            htt_parssed_manifesto: dict[str, Any] = parse_htt_file(
                htt_manifesto_request.text
            )

            # Run the custom tag link validation
            custom_tags_path = self.handle_htt_manifesto(htt_parssed_manifesto)

        print(
            f'A usar tags custom (local):\n -> <{custom_tags_path}>\n' + '-'*20
        )

        self.tags_custom: dict[str, os.DirEntry] = {}
        if custom_tags_path is not None:
            dir_entries: dict[str, os.DirEntry] | None = self.path_dir_entries(
                path=custom_tags_path
            )

            if dir_entries is not None:
                if cli_store_get('htt-config-fallback') is not None:
                    default_htt_configs = self.resolver_conteudo_ficheiro(
                        str(cli_store_get('htt-config-fallback'))
                    )

                    if parse_htt_file(
                        default_htt_configs
                    ).get(
                        'tags_custom'
                    ) is not None:
                        default_custom_tags_path = str(
                            parse_htt_file(
                                default_htt_configs
                            ).get('tags_custom')
                        )
                        default_custom_tags_entries: dict[str, os.DirEntry] | None = \
                            self.path_dir_entries(
                                path=default_custom_tags_path
                        )
                        if default_custom_tags_entries is not None:
                            dir_entries.update(
                                dir_entries,
                                **default_custom_tags_entries
                            )

                self.tags_custom.update(
                    dict(
                        (key, val) for key, val in dir_entries.items()
                        if key[key.index('.'):] in HTT_FILE_EXTENSIONS
                    )
                )

        print(
            f'Tags found: \n\t{", ".join(self.tags_custom.keys())}\n{"-"*20}')

        custom_tags: list[tuple[str, ...]] = []
        for _, ficheiro in self.tags_custom.items():
            custom_tags.append(
                tuple(
                    filter(
                        lambda x: x != '',
                        re.split(
                            r'<css>|<html>\n{1,}<css>|<html>',
                            self.resolver_conteudo_dir_entry(ficheiro)
                        )
                    )
                )
            )

        return dict(zip(self.tags_custom.keys(), custom_tags))

    async def resolve_htt_templates(self) -> None:
        """
        Resolve os ficheiros htt e retira a informação inerente aos mesmos
        """
        for chave, dir_entry in self.conteudo_dir.items():
            # só lê o ficheiro se não for um file de config ou uma pasta
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

    def __init__(self, adition_tags: dict[str, tuple[str, ...]] | None) -> None:
        # Adiciona as funcs disponiveis para gerar tags de html
        # através dos atributuos registados na class
        self.valid_tags: list[str] = [
            'h1', 'h2', 'h3',
            'h4', 'h5', 'p',
            'span', 'hr', 'a',
            'img', 'section',
        ]

        # Add custom tags
        self.valid_tags_custom: dict[
            str,
            tuple[str, ...]
        ] | None = adition_tags

    @ staticmethod
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

        if ".htt.custom" in tag and self.valid_tags_custom is None:
            print(f"No custom tags to use for <{tag}>!")
            return ''

        # check for custom tags
        if (
            self.valid_tags_custom is not None
            and '.htt.custom' in tag
            and tag in self.valid_tags_custom
        ):
            tag_content: str = self.valid_tags_custom[tag][0]
            # css style formatting for regex validation
            tag_style: str = ''.join(
                map(
                    lambda x: '\\n' if x == r'\n' else x,
                    self.valid_tags_custom[tag][1]
                )
            )

            css_style_pattern: re.Pattern = re.compile(
                r'\.[A-z-_]+\s{0,}\{.+\}', re.MULTILINE
            )

            refactored_css_style: str = ''.join(
                map(
                    lambda x: r'\n' if x == '\\n' else x,
                    tag_style
                )
            )

            # only add css classes
            if re.findall(css_style_pattern, tag_style) is not None:
                cli_store_set(
                    'custom-tags-css',
                    refactored_css_style
                )

            return f'<div id="{tag_id}">\n{tag_content}\n</div>'

        if tag not in self.valid_tags:
            erro_exit(
                menssagen=f'A tag fornecida não é válida <{tag}>',
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
            configs: TemplateConfig,
            custom_tags: dict[str, tuple[str, ...]] | None
    ):
        # Setup of html tag generator
        super().__init__(custom_tags)

        # htt templates
        self.templates: dict[str, TemplateFile] = htt_templates

        # Needed Templater functionalitty
        self.file_handeling: FileHandler = file_handeling
        self.configs: TemplateConfig = configs

        # End result folder
        self.output_pasta_path: str = self.file_handeling.criar_pasta(
            'htt-output'
        )

        # Corre de uma maneira asincrona e em uma threads
        asyncio.run(
            self.gen_html()
        )

    @ staticmethod
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
        Translate the htt file contents and write them to the html file
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

        novo_conteudo_ficheiro.append('<body>\n<main>\n')

        previous_content: str | None = CLI_STORE.get('custom-tags-css')

        # Itera sobre as secções no template
        for section_name, section in template.items():
            # Adiciona ao novo conteudo para o ficheiro html
            try:
                novo_conteudo_ficheiro.append(
                    # Chama as funções adequadas para as tags dadas
                    self.html_tag_resolve(
                        other_options=section,
                        tag=section['tag'],
                        tag_id=section_name,
                    )
                )
                current_custom_tags: str | None = \
                    CLI_STORE.get(
                        'custom-tags-css'
                    )

                if current_custom_tags is not None and current_custom_tags != previous_content:
                    self.update_css_style(current_custom_tags)
            except KeyError as err:
                erro_exit(
                    menssagen=f'O valor <{err}>, não foi fornecido',
                    tipo_erro='NotEnoughVals',
                    time_stamp=True
                )

        # Close html body
        novo_conteudo_ficheiro.append('\n</main>\n</body>')
        # Close html tag
        novo_conteudo_ficheiro.append('\n</html>')

        # Escreve o conteudo html no ficheiro
        self.file_handeling.escrever_conteudo_ficheiro(
            conteudo=novo_conteudo_ficheiro,
            ficheiro=ficheiro_path,
            modo='a+'
        )

    def update_css_style(self, content: str) -> None:
        """
        Atualiza o ficheiro de css com o conteudo fornecido
        """
        # Write css file to htt-output
        self.file_handeling.escrever_conteudo_ficheiro(
            modo='+a',
            ficheiro=self.__gen_css_file_path(),
            conteudo=content
        )

    def __get_css_file_path(self) -> str:
        """
        Get css theme file path
        """
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'css',
            (self.configs.tema + '.css')
        )

    def __gen_css_file_path(self) -> str:
        """
        Generates the css theme file path.
        """
        return os.path.join(
            self.output_pasta_path,
            (self.configs.tema + '.css')
        )

    def insert_css_style(self) -> None:
        """
        Cria o ficheiro de estilo defenido através
        da opção "tema" no ficheiro .htt-config,
        para a pasta de output "htt-output"
        """
        # Write css file to htt-output
        self.file_handeling.escrever_conteudo_ficheiro(
            modo='w',
            ficheiro=self.__gen_css_file_path(),
            conteudo=self.file_handeling.resolver_conteudo_ficheiro(
                self.__get_css_file_path()
            )
        )

    async def gen_html(self) -> None:
        """
        'Transpila' os conteudos dos templates htt, para html e css
        de uma maneira asyncrona e threaded
        """

        # Add css style
        self.insert_css_style()

        # Ao utilizar o loop das running tasks, posso adicionar tasks ao mesmo loop,
        # sem bloquear o loop que itera pelos templates, e o loop das tasks

        # Get the running tasks @ loop
        async_new_file_gen_running_loop = asyncio.get_running_loop()

        # Get templates to transpile
        for template_name, template_file in self.templates.items():
            async_new_file_gen_running_loop.create_task(
                # Create a new task for a new file
                # And make that task run on a new thread
                asyncio.to_thread(
                    self.transpile_htt_to_html,
                    template_name,
                    template_file
                )
            )
