"""
Configurações do templating
"""

from file_handeling.handler import parse_htt_file


class Configs:
    """
    Gere e armazena as configurações para o templating
    do site a gerar
    """

    def __init__(self, conteudo: str):
        # Configs Esperadas
        self.fontes: dict[str, str] = {}
        self.tema: str = ''
        self.estilo: str = ''
        self.tags_custom: str = ''
        # End Configs Esperadas

        #  Adiciona os valores e atributuos corretos à class
        for chave, valor in parse_htt_file(conteudo).items():
            self.__setattr__(chave, valor)

        for some in self.config_opcoes():
            print(f'{self.__getattribute__(some)=}, {some=}')

    def config_opcoes(self) -> list[str]:
        """
        Retorna os valores de config existentes na class

        Returns:
            list[str]: Valores disponiveis
        """
        return list(
            map(
                lambda x: x.replace('__', ''),
                self.__dict__
            )
        )

    def config_valores(self) -> list[any]:
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

        self._config_obj: Configs = super()
        self.configs: dict[str, any] = self.configuracao_template()

    def configuracao_template(self) -> dict[str, any]:
        """
        Retorna um dicionario com a configuração do template

        Returns:
            dict[str, any]: Valores de configuração ligados por key/val
        """
        return zip(
            self._config_obj.config_opcoes(),
            self._config_obj.config_valores()
        )

    def opcoes_config_existentes(self) -> list[str]:
        """
        Devolve as keys existentes no ficheiro de configuração

        Returns:
            list[str]: [description]
        """
        return self._config_obj.config_opcoes()

    def valores_config_existentes(self) -> list[str]:
        """
        Devolve os valores existentes para as configurações defenidas

        Returns:
            list[str]: [description]
        """
        return self._config_obj.config_valores()
