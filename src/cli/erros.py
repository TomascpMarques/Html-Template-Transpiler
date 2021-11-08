"""
O módulo gere as menssagens de erro a devolver ao user, e como as devolver
"""

import sys
import time


def erro_exit(menssagen: str, tipo_erro: str = "Erro", time_stamp: bool = False) -> None:
    """[summary]

    Args:
        menssagen (str): [description]
        tipo_erro (str, optional): [description]. Defaults to "Erro".
        time_stamp (bool, optional): [description]. Defaults to False.
    """
    sys.exit(
        f'{tipo_erro}{" @ " + time.strftime("%H:%M:%S") if time_stamp else "" }:\n| {menssagen}\n'
    )
