import asyncio
import logging
from typing import AsyncIterator

import aiohttp.web

from .database.database import Database
from .protocols.http import HTTP
from .proxy import Proxy
from .settings import Settings, SettingsError
from .ui import setup_app


async def listen(app: aiohttp.web.Application) -> AsyncIterator[None]:
    tasks = [asyncio.create_task(proxy.start()) for proxy in app["proxies"]]
    if len(tasks):
        await asyncio.wait(tasks)
    yield


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    app = setup_app()
    app["settings"] = Settings()
    try:
        app["settings"].load()
    except SettingsError as error:
        logging.error(error)
        exit(1)
    app["database"] = Database()
    app["proxies"] = []
    for proxy in app["settings"].proxies:
        if proxy.protocol == "http":
            app["proxies"].append(Proxy(app["database"], proxy, HTTP))
    app.cleanup_ctx.append(listen)
    return app


def main():
    app = create_app()
    settings = app["settings"]
    aiohttp.web.run_app(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
