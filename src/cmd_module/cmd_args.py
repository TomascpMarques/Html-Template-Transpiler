"""
Contêm os argumentos disponíveis para uso pela cmd
"""


from dataclasses import dataclass, field
import re


@dataclass
class CmdArgument:
    """
    Define a estrutura de um possivél argumento aceitável pela aplicação/cmd
    """
    key: str = field(default_factory=str,)
    value_type: type = field(default_factory=str)
    validation_template: re.Pattern = field(default=re.compile('--\w+\s'))


CMD_ARGS: list[CmdArgument] = [
    CmdArgument('file', str),
    CmdArgument('s', str)
]
