import abc
import asyncio

import redis.asyncio as redis

from battleship.server.pubsub import IncomingChannel, OutgoingChannel
from battleship.server.repositories.observable import Observable
from battleship.server.websocket import Client
from battleship.shared.models import Action
from battleship.shared.models import Client as ClientModel


class ClientNotFound(Exception):
    pass


class ClientRepository(Observable, abc.ABC):
    def __init__(self, incoming_channel: IncomingChannel, outgoing_channel: OutgoingChannel):
        super().__init__()
        self._in_channel = incoming_channel
        self._out_channel = outgoing_channel

    @abc.abstractmethod
    async def add(self, client_id: str, nickname: str, guest: bool, version: str) -> Client:
        pass

    @abc.abstractmethod
    async def get(self, client_id: str) -> Client:
        pass

    @abc.abstractmethod
    async def list(self) -> list[Client]:
        pass

    @abc.abstractmethod
    async def delete(self, client_id: str) -> bool:
        pass

    @abc.abstractmethod
    async def clear(self) -> int:
        pass

    @abc.abstractmethod
    async def count(self) -> int:
        pass


class InMemoryClientRepository(ClientRepository):
    def __init__(
        self, incoming_channel: IncomingChannel, outgoing_channel: OutgoingChannel
    ) -> None:
        super().__init__(incoming_channel, outgoing_channel)
        self._clients: dict[str, Client] = {}

    async def add(self, user_id: str, nickname: str, guest: bool, version: str) -> Client:
        client = Client(user_id, nickname, guest, version, self._in_channel, self._out_channel)
        self._clients[client.id] = client
        self._notify_listeners(client.id, Action.ADD)
        return client

    async def get(self, client_id: str) -> Client:
        try:
            return self._clients[client_id]
        except KeyError:
            raise ClientNotFound(f"Client {client_id} doesn't exist.")

    async def list(self) -> list[Client]:
        return list(self._clients.values())

    async def delete(self, client_id: str) -> bool:
        self._notify_listeners(client_id, Action.REMOVE)
        return self._clients.pop(client_id, None) is not None

    async def clear(self) -> int:
        client_count = 0

        while True:
            try:
                self._clients.popitem()
                client_count += 1
            except KeyError:
                break

        return client_count

    async def count(self) -> int:
        return len(self._clients)


class RedisClientRepository(ClientRepository):
    key = "clients"
    namespace = key + ":"
    pattern = namespace + "*"

    def __init__(
        self,
        client: redis.Redis,
        incoming_channel: IncomingChannel,
        outgoing_channel: OutgoingChannel,
    ) -> None:
        super().__init__(incoming_channel, outgoing_channel)
        self._client = client

    def get_key(self, client_id: str) -> str:
        return f"{self.namespace}{client_id}"

    def get_client_id(self, key: str | bytes) -> str:
        if isinstance(key, bytes):
            key = key.decode()

        return key.removeprefix(self.namespace)

    async def add(self, client_id: str, nickname: str, guest: bool, version: str) -> Client:
        client = Client(client_id, nickname, guest, version, self._in_channel, self._out_channel)
        await self._save(client)
        self._notify_listeners(client.id, Action.ADD)
        return client

    async def get(self, client_id: str) -> Client:
        data = await self._client.get(self.get_key(client_id))

        if data is None:
            raise ClientNotFound(f"Client {client_id} not found.")

        model = ClientModel.from_raw(data)
        return Client(
            model.id,
            model.nickname,
            model.guest,
            model.version,
            self._in_channel,
            self._out_channel,
        )

    async def list(self) -> list[Client]:
        keys = await self._client.keys(self.pattern)
        get_futures = [self.get(self.get_client_id(key)) for key in keys]
        return await asyncio.gather(*get_futures)

    async def delete(self, client_id: str) -> bool:
        result = bool(await self._client.delete(self.get_key(client_id)))
        self._notify_listeners(client_id, Action.REMOVE)
        return result

    async def clear(self) -> int:
        keys: list[str] = await self._client.keys(self.pattern)

        if len(keys):
            count: int = await self._client.delete(*keys)
            return count
        return 0

    async def count(self) -> int:
        keys = await self._client.keys(self.pattern)
        return len(keys)

    async def _save(self, client: Client) -> bool:
        model = ClientModel(
            id=client.id, nickname=client.nickname, guest=client.guest, version=client.version
        )
        return bool(await self._client.set(self.get_key(client.id), model.to_json()))
