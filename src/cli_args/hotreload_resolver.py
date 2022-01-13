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
from dataclasses import dataclass

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

    try:
        asyncio.run(
            start_hotreload_process(
                setup_file_waching(
                    watchable_files
                )
            )
        )
    except KeyboardInterrupt:
        print('\nA sair do modo de hot reloading...\n')
        return


@dataclass(slots=True, init=True)
class MinifiedFileInfo():
    """
    Minified file information
    """
    name: str       # name of the file
    path: str       # path of the file
    hashed: int     # hash of the file


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
                    print(f'[+] RELOADING... File changed «{entry.name}»;')
                    entry.hashed = file_hashed_content
                    project_reload()

        await asyncio.sleep(0.8)


def project_reload() -> None:
    """
    Reloads the project, with the same arguments as previously ran
    """
    os.chdir(
        str(cli_store_get('base_path'))
    )

    reload_command = ' '.join(sys.orig_argv[
        :sys.orig_argv.index('--hotreload')
    ])

    os.system(reload_command)


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
    descricao_argumento='Deteta mudanças nos ficheiros do projeto, e reconstroi os ficheiros',
    run=run_arg_hotreload,
    erro_validacao='Não foi possivél reconstruir o projeto',
    mensagem_ajuda=files_mens_ajuda,
    re_validacao_tipo_valor=re.compile(
        r'sim'
    ),
)
