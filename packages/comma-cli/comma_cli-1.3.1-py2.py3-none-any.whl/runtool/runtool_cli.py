from __future__ import annotations

import logging
import os
from typing import List

import typer

from runtool import RUNTOOL_CONFIG


app_run = typer.Typer(name='run', help='Run Tool.')


# @sqlite_cache(minutes=1)
def _tools() -> List[str]:
    return list(RUNTOOL_CONFIG.tools())


@app_run.command(
    add_help_option=False,
    no_args_is_help=True,
    context_settings={
        'allow_extra_args': True,
        'ignore_unknown_options': True,
    },
)
def run(
    ctx: typer.Context,
    tool: str = typer.Argument(..., autocompletion=_tools, help=f'{" ".join(_tools())}'),
    which: bool = typer.Option(False, '--which', help='Print the command instead of running it.'),
) -> int:
    """
    Installs (if needed) and runs a tool.
    """
    try:
        tool_path = RUNTOOL_CONFIG[tool].get_executable()
        # RunToolConfig.get_instance().save()
    except KeyError:
        if tool == '--help':
            print(ctx.get_help())
        else:
            logging.error(f'No tool named: {tool}')
        return 1
    if which:
        print(tool_path)
        return 0
    cmd = (tool_path, *ctx.args)
    os.execvp(cmd[0], cmd)


if __name__ == '__main__':
    app_run()
