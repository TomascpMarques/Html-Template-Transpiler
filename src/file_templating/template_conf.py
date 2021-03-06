"""
Configurações do templating
"""

from dataclasses import dataclass
from typing import Any, Literal
from file_handeling.handler import parse_htt_file


@dataclass(slots=True)
class Configs():
    """
    Gere e armazena as configurações para o templating
    do site a gerar
    """

    def __init__(self, conteudo: str):
        # Configs Esperadas
        self.fontes: dict[str, str] = {}
        self.tema: str = ''
        self.estilo: str = ''
        # End Configs Esperadas

        # O atributuo tags_custom, só é adicionado pelo conteudo do ficheiro
        # não é adicionado por defeito.

        #  Adiciona os valores e atributuos corretos à class
        for chave, valor in parse_htt_file(conteudo).items():
            self.__setattr__(chave, valor)

    def get_config_valor(self, config_key: str) -> Any | Literal[None]:
        """
            Retorna a config pedida pela key

            Args:
                config_key (str): String for the config value to query

            Returns:
                Any: O valor da config pedida
        """
        try:
            return self.__getattribute__(config_key)
        except AttributeError:
            return None

    def config_opcoes(self) -> list[str]:
        """
        Retorna os valores de config existentes na class

        Returns:
            list[str]: Valores disponiveis
        """
        # Todos os atributuos que se quer usar como configs
        # são os que não contêm «_»
        return list(
            filter(
                lambda x: '__' not in x,
                self.__dict__
            )
        )

    def config_valores(self) -> list:
        """
        Retorna uma lista só com todos os valores
        de todas as opções de config_opcoes

        Returns:
            list[any]: Valores de configuração
        """
        return list(
            self.__getattribute__(valor)
            for valor in self.config_opcoes()
        )


class TemplateConfig(Configs):
    """
    Centraliza e manipula as configurações do projeto
    """

    def __init__(self, conf_file: str):
        # Init do objeto Config para uso
        super().__init__(conf_file)

        self.template_configs = self.configuracao_template()

    def configs(self) -> dict[str, Any]:
        """
        Devolve todos os valores atribuidos à configuração de template

        Returns:
            dict[str, any]: Keys and values in a dict
        """
        return self.__dict__

    def configuracao_template(self) -> dict[str, Any]:
        """
        Retorna um dicionario com a configuração do template

        Returns:
            dict[str, any]: Valores de configuração ligados por key/val
        """
        return dict(
            zip(
                self.config_opcoes(),
                self.config_valores()
            )
        )

    def opcoes_config_existentes(self) -> list[str]:
        """
        Devolve as keys existentes no ficheiro de configuração

        Returns:
            list[str]: [description]
        """
        return self.config_opcoes()

    def valores_config_existentes(self) -> list[str]:
        """
        Devolve os valores existentes para as configurações defenidas

        Returns:
            list[str]: [description]
        """
        return self.config_valores()
