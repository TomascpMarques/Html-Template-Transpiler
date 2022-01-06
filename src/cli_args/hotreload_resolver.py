"""
This module deals with hot reloading of project files.
The files under the project directory will be watched for changes.
And if any changes occur they will be recompiled.
"""

import os
import re
import sys
from typing import Iterable, Any
import asyncio

from cli.arg_setup import CliArgumento
from cli_store.store import cli_store_get


def run_arg_hotreload(_: str, **_kwargs: Any) -> None:
    """
    Sets up the file reloading, if changes are detected
    """

    project_dir: str | None = cli_store_get('htt-project')
    if project_dir is None:
        print('No project directory specefied, cant watch files.')
        return

    print(f'{"-"*10} A começar «project hot_reloading» {"-"*10}\n')

    watchable_files: list[os.DirEntry] = []
    found_files: Iterable[os.DirEntry] = os.scandir(project_dir)

    for entry in found_files:
        if entry.is_file() and entry.name[-4:] == '.htt':
            watchable_files.append(entry)

    print(f'{"-"*10}\n Ficheiros encontrados:')
    for entry in watchable_files:
        print(f'-> {entry.name}')
    print(f'{"-"*10}\n')

    asyncio.run(
        start_hotreload_process(
            setup_file_waching(
                watchable_files
            )
        )
    )


class MinifiedFileInfo():
    """
    Minified file information
    """

    def __init__(self, name: str, path: str, hashed: int) -> None:
        self.name = name
        self.path = path
        self.hashed = hashed


def setup_file_waching(files: list[os.DirEntry]) -> list[MinifiedFileInfo]:
    """
    Minifies the infor of the files being watched,
    only storing the name, the path and the path for the files
    """
    file_watcher_info: list[MinifiedFileInfo] = []

    for entry in files:
        with open(entry.path, 'r', encoding='utf-8') as file:
            file_watcher_info.append(
                MinifiedFileInfo(
                    entry.name,
                    entry.path,
                    hash(file.read())
                )
            )

    return file_watcher_info


async def run_file_watcher(file_watcher_info: list[MinifiedFileInfo]) -> None:
    """
    Watches for file changes, reloads the project
    """
    while True:
        for entry in file_watcher_info:
            with open(entry.path, 'r', encoding='utf-8') as file:
                file_hashed_content = hash(file.read())
                if entry.hashed != file_hashed_content:
                    print(f'File changed «{entry.name}»; [+] RELOADING...')
                    entry.hashed = file_hashed_content
                    project_reload()

        await asyncio.sleep(0.8)


def project_reload() -> None:
    """
    Reloads the project, with the same arguments as previously ran
    """
    os.system(
        ' '.join(sys.orig_argv[
            1:sys.argv.index('--hotreload')
        ])
    )


async def start_hotreload_process(file_watcher_info: list[MinifiedFileInfo]) -> None:
    """
    Starts the asynchronous process
    """
    await asyncio.get_event_loop().create_task(
        await asyncio.to_thread(
            run_file_watcher,
            file_watcher_info
        )
    )

files_mens_ajuda: str = \
    '* Parametro: <hotreload> | Exemplo: --hotreload sim\n'


hotreload_arg: CliArgumento = CliArgumento(
    chave='hotreload',
    descricao_argumento='Deteta mudanças nos ficheiros do projeto',
    run=run_arg_hotreload,
    erro_validacao='Não foi possivél reconstruir o projeto',
    mensagem_ajuda=files_mens_ajuda,
    re_validacao_tipo_valor=re.compile(
        r'sim'
    ),
)
