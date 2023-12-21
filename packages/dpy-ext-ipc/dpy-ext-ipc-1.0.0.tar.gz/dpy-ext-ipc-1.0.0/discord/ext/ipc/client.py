from __future__ import annotations

import asyncio

from typing import Optional, Union, Literal

from logging import getLogger, Logger

from discord.client import Client
from discord.http import HTTPClient
from discord.utils import setup_logging

from discord.user import User
from discord.guild import Guild
from discord.abc import GuildChannel, PrivateChannel
from discord.threads import Thread

from quart import Quart

class IPC:
    """Represents an IPC session.
    
    All the methods here are API calls, and the get methods uses
    the client caché, so they may return `None`.

    Parameters
    ----------
    client: :class:`Client`
        The client this session is linked to.
    host: :class:`str`
        The host the web-app side will listen to. Defaults to `localhost`
    port: :class:`int`
        The port the web-app side will listen to. Defaults to `8080`
    debug: :class:`bool`
        If the console should autorestart the web server when changes are made.
        Defaults to `False`
    app: Optional[:class:`Quart`]
        A already instated Quart App that the IPC will use.
    """

    def __init__(self, client: Client, *, host: str = '127.0.0.1', port: int = 8000, debug: bool = False, app: Optional[Quart] = None) -> None:
        self.client: Client = client
        self.host: str = host
        self.port: int = port
        self.debug: bool = debug

        self._app: Quart = app or Quart('discord.ext.ipc.server')

        self.is_closed: bool = True

        self._setattrs()

    @property
    def app(self) -> Quart:
        """:class:`Quart`: Returns the Web-app Side of the client."""
        return self._app

    def _setattrs(self) -> None:
        self.http: HTTPClient = self.client.http
        self._log: Logger = getLogger('discord')
        self._log.name = 'discord.ext.ipc.client'

    async def _start_connection(self) -> None:
        self.is_closed: bool = False

        self._log.info('started IPC app connection')
        self.app.run(self.host, self.port, debug=self.debug, loop=self.client.loop)

    async def __aenter__(self) -> IPC:
        await self.start()
        return self

    async def start(self) -> None:
        """|coro|
        
        Starts running the IPC.

        This should be done asynchronously with `client.start`.

        If you want to run both using a method, consider using `run`
        """
        if hasattr(self.client, 'on_ipc_start'):
            await self.client.on_ipc_start(self)

        await self._start_connection()

    def run(self, token: str, **kwargs) -> None:
        """Starts running both the linked client and the IPC server.
        
        Parameters
        ----------
        token: class:`str`
            The authentication token. Do not prefix this token with
            anything as the library will do it for you.
        """

        async def runner():
            setup_logging()
            await asyncio.gather(
                self.client.start(token, reconnect=kwargs.pop('reconnect', True)),
                self.app.run_task(self.host, self.port, debug=self.debug,)
            )


        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return # asyncio handles this
        
    def get(self, obj: Literal['guild', 'channel', 'user'], id: int) -> Optional[Union[GuildChannel, Thread, PrivateChannel, User, Guild]]:
        """Gets and returns the object with id X
        from the cache.

        Parameters
        ----------
        obj: :class:`str`
            The object to get.
        id: :class:`int`
            The id of the object to get.
        """

        getter = getattr(self.client, f'get_{obj}')
        return getter(id)
    
    async def fetch(self, obj: Literal['guild', 'channel', 'user'], id: int) -> Optional[Union[GuildChannel, Thread, PrivateChannel, User, Guild]]:
        """|coro|
        
        Fetches and returns the given object with id X.

        Parameters
        ----------
        obj: :class:`str`
            The object to fetch.
        id: :class:`int`
            The id of the object to fetch.
        """

        fetcher = getattr(self.client, f'fetch_{obj}')
        return await fetcher(id)
    
    async def get_or_fetch(self, obj: Literal['guild', 'channel', 'user'], id: int) -> Optional[Union[GuildChannel, Thread, PrivateChannel, User, Guild]]:
        """|coro|
        
        Gets or fetches the given object with id X.

        This tries to get the object, if it is `None`,
        then it tries to fetch it.

        Parameters
        ----------
        obj: :class:`str`
            The object to get or fetch
        id: :class:`int`
            The id of the object to get or fetch
        """

        try:
            value = self.get(obj, id)

            if not value:
                value = await self.fetch(obj, id)

            return value
        
        except Exception as e:
            self._log.error('ignoring exception in get_or_fetch:\n%s', e)
