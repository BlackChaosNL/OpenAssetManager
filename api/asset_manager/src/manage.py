#!/usr/bin/env python3

from ptpython.repl import embed, ReplExit

import asyncio, importlib, contextlib, sys, os, tomllib, asyncclick

from database import migrate_db
from pathlib import Path
from asyncclick import BadOptionUsage, ClickException
from collections.abc import AsyncGenerator
from tortoise import Tortoise, connections

#
# Custom implementation of Tortoise CLI
# Original script is located under: https://github.com/tortoise/tortoise-cli
# License: Apache-2.0 as dictated as [here](https://github.com/tortoise/tortoise-cli/blob/main/LICENSE)
#


def tortoise_orm_config(file="pyproject.toml") -> str:
    """
    get tortoise orm config from os environment variable or aerich item in pyproject.toml

    :param file: toml file that aerich item loads from it
    :return: module path and var name that store the tortoise config, e.g.: 'settings.TORTOISE_ORM'
    """
    if not (config := os.getenv("TORTOISE_ORM", "")) and (p := Path(file)).exists():
        doc = tomllib.loads(p.read_text("utf-8"))
        config = doc.get("tool", {}).get("aerich", {}).get("tortoise_orm", "")
    return config


def get_tortoise_config(config: str) -> dict:
    """
    get tortoise config from module
    :param ctx:
    :param config:
    :return:
    """
    splits = config.split(".")
    config_path = ".".join(splits[:-1])
    tortoise_config = splits[-1]

    try:
        config_module = importlib.import_module(config_path)
    except ModuleNotFoundError as e:
        raise ClickException(
            f"Error while importing configuration module: {e}"
        ) from None
    c = getattr(config_module, tortoise_config, None)
    if not c:
        raise BadOptionUsage(
            option_name="--config",
            message=f'Can\'t get "{tortoise_config}" from module "{config_module}"',
            ctx=None,
        )
    return c


@contextlib.asynccontextmanager
async def aclose_tortoise() -> AsyncGenerator[None]:
    try:
        yield
    finally:
        if Tortoise._inited:
            await connections.close_all()

def history():
    import readline
    for i in range(1, readline.get_current_history_length()+1):
        print("%3d %s" % (i, readline.get_history_item(i)))

async def setup():
    if not (config := tortoise_orm_config()):
        raise asyncclick.UsageError(
            "You must specify TORTOISE_ORM in option or env, or config file pyproject.toml from config of aerich",
            ctx=None,
        )
    await migrate_db(get_tortoise_config(config))

    async with aclose_tortoise():
        await embed(
            globals=globals(),
            title="shell",
            vi_mode=True,
            return_asyncio_coroutine=True,
            patch_stdout=True,
        )


if __name__ == "__main__":
    if sys.path[0] != ".":
        sys.path.insert(0, ".")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        history()
        loop.run_until_complete(asyncio.ensure_future(setup()))
    except (KeyboardInterrupt, ReplExit) as e:
        print(e)
        loop.stop()

