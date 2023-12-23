from __future__ import annotations
from inspect import iscoroutinefunction, signature
from datetime import datetime

from socketio import AsyncClient
import asyncio
import re

from sarya import UI
from sarya.request_typings import NewMessage, Response

class Sarya:

    def __init__(self, key: str | None = None):
        self.key = key
        self.sio = AsyncClient()
        self.marid_handlers = []
        self.sio.on("connection_log")(self.connection_log)

    async def _run(self):
        await self.sio.connect(
            "https://api.sarya.com",
            headers={
                "x-dev-secret": self.key,
                "handlers": "_".join(self.marid_handlers),
            },
            transports=["websocket"],
            socketio_path="/marid-socket/socket.io",
        # )
            wait_timeout=60)
        await self.sio.wait()

    def run(self):
        asyncio.run(self._run())
    
    def _process_response(self, response):
        if isinstance(response, Response):
            return response
        elif isinstance(response, UI.Text) or isinstance(response, UI.Image):
            return Response(messages=[response])
        elif isinstance(response, list):
            return Response(messages=response)
        return Response(messages=[response])

    def _process_handler_input(self, func, user_message):
        if (params := len(signature(func).parameters)) == 2:
            return [user_message.messages, user_message.meta]
        elif params == 1:
            return [user_message.messages]
        else:
            return []

    def app(self, func):
        marid_handler = re.sub(r"_", "-", func.__name__.lower())
        self.marid_handlers.append(marid_handler)
        @self.sio.on(marid_handler)
        async def wrapper(data):
            try:
                user_message = NewMessage(**data)
            except:
                print(f"we got error while trying to process {data}")
                return Response(messages=[UI.Text("something went wrong")]).model_dump(mode="json")
            if iscoroutinefunction(func):
                response = await func(*self._process_handler_input(func, user_message))
            else:
                response = func(*self._process_handler_input(func, user_message))
            return self._process_response(response).model_dump(mode="json")
        return wrapper

    async def connection_log(self, data):
        print(f"{datetime.now()}: HANDLER|{data.get('handler')} -> {data.get('message')}. STATUS: {data.get('status')}")