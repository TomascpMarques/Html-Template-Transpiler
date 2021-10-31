"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""


from file_handeling.handler import FileHandler


class TemplateFiles(FileHandler):
    """
    Some Some
    """

    def __init__(self, path: str):
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        self.stuff = 'temp'
