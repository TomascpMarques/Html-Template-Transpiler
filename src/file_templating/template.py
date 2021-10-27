"""
    Configurações para o templating usar,
    tais como tipo de letra, tema a usar e tipo de transpilação
"""

from file_handeling.handler import FileHandler
from file_templating.template_conf import TemplateConfig

TEMPLATE_CONFIG: str = '.httconfig'


class Templater(FileHandler):
    """
    Some Some
    """

    def __init__(self, path: str) -> None:
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        self.configs: TemplateConfig = TemplateConfig(
            super().resolver_ficheiro(TEMPLATE_CONFIG)
        )
