"""
    Configurações para o templating usar,
    tais como tipo de letra, tema a usar e tipo de transpilação
"""

import re
import requests
from cli.erros import erro_exit

from file_handeling.handler import FileHandler
from file_templating.template_conf import TemplateConfig
from file_templating.template_files import TemplatingFiles

HTT_CONFIG_FILE = '.httconfig'


class Templater(FileHandler):
    """
    Cria um objeto Templater para lidar com o templating e transpilação do projeto.

    Args:
        FileHandler ([type]): Objeto que gere ficheiros e pastas
    """

    def __init__(self, path: str, config_file_path: str) -> None:
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        regex_pattern: re.Pattern = re.compile(
            r'\S+\/\w+\.httconfig$'
        )

        # Configs defenition
        self.configs: TemplateConfig

        # Templating Configs
        if re.match(regex_pattern, config_file_path) is not None:
            req: requests.Response = requests.get(
                f'https://raw.githubusercontent.com/{config_file_path}'
            )

            # Verifies response
            if req.status_code != 200:
                erro_exit(
                    menssagen=f'O link fornecido para conf. não é válido: «{config_file_path}»'
                )

            # Verifies response content expected len
            if req.text.__len__() <= 1:
                erro_exit(
                    menssagen='O ficheiro de configs está vazio'
                )

            # Set up the configs
            self.configs = TemplateConfig(
                req.text
            )
        else:
            self.configs = TemplateConfig(
                # super()'s method
                self.resolver_conteudo_ficheiro(
                    config_file_path
                )
            )

        # Init Project templating
        self.templating: TemplatingFiles = TemplatingFiles(
            path=path,
            configs=self.configs
        )
