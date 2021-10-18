"""
O módulo gere as menssagens de erro a devolver ao user, e como as devolver
"""

import sys
import time


def exit(menssagen: str, tipo_erro: str = "Erro", time_stamp: bool = False) -> None:
    sys.exit(
        f'{tipo_erro}{" @ " + time.strftime("%H:%M:%S") if time_stamp else "" }:\n| {menssagen}\n'
    )


CMD_ERROS: dict = {}
