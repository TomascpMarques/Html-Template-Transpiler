"""
    Configurações para o templating usar,
    tais como tipo de letra, tema a usar e tipo de transpilação
"""

from file_handeling.handler import FileHandler
from file_templating.template_conf import TemplateConfig
from file_templating.template_files import TemplatingFiles

NOME_TEMPLATE_CONFIG: str = '.httconfig'


class Templater(FileHandler):
    """
    Cria um objeto Templater para lidar com o templating e transpilação do projeto.

    Args:
        FileHandler ([type]): Objeto que gere ficheiros e pastas
    """

    def __init__(self, path: str) -> None:
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        # Templating Configs
        self.configs: TemplateConfig = TemplateConfig(
            # super() method
            self.resolver_conteudo_ficheiro(NOME_TEMPLATE_CONFIG)
        )

        # Init Project templating
        self.templating: TemplatingFiles = TemplatingFiles(
            path=path,
            configs=self.configs
        )
