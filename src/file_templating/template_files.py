"""
    Este módulo lida com os ficheiros de templating,
    Ler os mesmos, e interpretalos
"""

from dataclasses import dataclass

from file_handeling.handler import FileHandler, parse_htt_file


class TemplatingFiles(FileHandler):
    """
    Some Some
    """

    def __init__(self, path: str):
        # Setup do FileHandler, com o caminho especifico
        super().__init__(path)

        self.conteudo_dir = super().conteudo_dir()
        self.htt_templates: dict[str, any] = {}

        for key, dir_entry in self.conteudo_dir.items():
            if '.httconfig' not in key and dir_entry.is_file():
                self.htt_templates.setdefault(
                    key,
                    TemplateFile(
                        parse_htt_file(
                            super().
                            resolver_conteudo_ficheiro(dir_entry.path)
                        )
                    ),
                )


@dataclass
class TemplateFile:
    """
    Some Some
    """

    def __init__(self, file_tags: dict[str, list[str]]):
        for key, valor in file_tags.items():
            self.__setattr__(key, valor)

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
