#!/usr/bin/env python3

from ptpython.repl import embed  # type: ignore

from database import *

import asyncio


async def setup():
    try:
        await embed(globals=globals(), return_asyncio_coroutine=True, patch_stdout=True)
    except EOFError:
        loop.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.ensure_future(setup())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
