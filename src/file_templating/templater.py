"""
    Configurações para o templating usar,
    tais como tipo de letra, tema a usar e tipo de transpilação
"""

from file_handeling.handler import FileHandler
from file_templating.template_conf import TemplateConfig
from file_templating.template_files import TemplatingFiles

TEMPLATE_CONFIG_NOMEACAO: str = '.httconfig'


class Templater(FileHandler):
    """
    Cria um objeto Templater para lidar com o templating e transpilação do projeto.

    Args:
        FileHandler ([type]): Objeto que gere ficheiros e pastas
    """

    def __init__(self, path: str) -> None:
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        self.configs: TemplateConfig = TemplateConfig(
            super().resolver_conteudo_ficheiro(TEMPLATE_CONFIG_NOMEACAO)
        )

        self.templating: TemplatingFiles = TemplatingFiles(
            path=path,
            configs=self.configs
        )
