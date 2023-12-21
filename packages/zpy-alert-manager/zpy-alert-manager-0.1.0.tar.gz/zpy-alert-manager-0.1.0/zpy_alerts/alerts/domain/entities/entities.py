from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, Any
from time import time

T = TypeVar('T')


@dataclass
class Identity:
    username: Optional[str]
    user_id: Optional[str]


@dataclass
class Device:
    name: Optional[str]
    model: Optional[str]
    os: Optional[str]


@dataclass
class ClientApplication:
    version: Optional[str]


@dataclass
class HostApplication:
    name: Optional[str]
    version: Optional[str]


@dataclass
class AlertContext:
    identity: Identity
    device: Device
    client_app: ClientApplication
    host_app: HostApplication


@dataclass
class AlertNotifier:
    name: str
    channels: list[str]


@dataclass
class AlertConfiguration:
    notifiers: list[AlertNotifier]
    ttl: int


@dataclass
class Alert(Generic[T]):
    type: str
    origin: str
    created_at: str
    criticality: str
    config: AlertConfiguration
    context: AlertContext
    data: T


class AlertRawData:
    TYPE_KEY: str = 'type'
    CRITICALITY_KEY: str = 'criticality'
    ORIGIN_KEY: str = 'origin'
    CREATED_AT_KEY: str = 'created_at'
    CONFIG_KEY: str = 'config'
    CONTEXT_KEY: str = 'context'
    CONTEXT_REQUEST_ID_KEY: str = 'request_id'
    CONFIG_TTL_KEY: str = 'ttl'
    CONFIG_NOTIFIERS_KEY: str = 'notifiers'
    CONFIG_NOTIFIERS_CHANNELS_KEY: str = 'channels'
    MISSING_VALUE: str = '[NOT SPECIFIED]'
    DEFAULT_NOTIFIER_CHANNEL: list[str] = ['default']

    def __init__(self, raw: dict) -> None:
        self.data = raw

    def get_context(self) -> dict:
        if not self.data or self.CONTEXT_KEY not in self.data:
            return {}
        return self.data[self.CONTEXT_KEY]

    def get_context_request_id(self) -> str:
        ctx = self.get_context()
        return ctx.get(self.CONTEXT_REQUEST_ID_KEY, self.MISSING_VALUE)

    def get_config_channels_of_notifier(self, notifier_name: str):
        if self.data is None or self.CONFIG_KEY not in self.data:
            return self.DEFAULT_NOTIFIER_CHANNEL
        if self.CONFIG_NOTIFIERS_KEY not in self.data[self.CONFIG_KEY]:
            return self.DEFAULT_NOTIFIER_CHANNEL

        notifier = AlertRawData.__find_notifier(self.data[self.CONFIG_KEY][self.CONFIG_NOTIFIERS_KEY], notifier_name)
        if not notifier or self.CONFIG_NOTIFIERS_CHANNELS_KEY not in notifier:
            return self.DEFAULT_NOTIFIER_CHANNEL

        return notifier.get(self.CONFIG_NOTIFIERS_CHANNELS_KEY, self.DEFAULT_NOTIFIER_CHANNEL)

    @staticmethod
    def __find_notifier(notifiers: list[dict], name: str) -> dict | None:
        if not notifiers:
            return None
        results = list(filter(lambda notifier: notifier['name'] == name, notifiers))
        if not results:
            return None
        return results[0]

    def get_alert_info(self) -> str:
        return f'{self.get_type()}-{self.get_origin()}'

    def get_type(self) -> str:
        if not self.data:
            return self.MISSING_VALUE
        return self.data.get(self.TYPE_KEY, self.MISSING_VALUE)

    def get_origin(self) -> str:
        if not self.data:
            return self.MISSING_VALUE
        return self.data.get(self.ORIGIN_KEY, self.MISSING_VALUE)

    def get_config_ttl(self, default_ttl: int) -> int:
        if self.data is None or self.CONFIG_KEY not in self.data:
            return default_ttl

        if self.CONFIG_TTL_KEY not in self.data[self.CONFIG_KEY] or self.data[self.CONFIG_KEY][
            self.CONFIG_TTL_KEY] is None:
            return default_ttl

        return int(self.data[self.CONFIG_KEY][self.CONFIG_TTL_KEY])

    def get_created_at(self) -> int:
        if self.data is None or self.CREATED_AT_KEY not in self.data:
            return int(time())

        if self.data[self.CREATED_AT_KEY] is None:
            return int(time())

        return int(self.data[self.CREATED_AT_KEY])

    def get_criticality_level(self) -> str:
        if self.data is None or self.CRITICALITY_KEY not in self.data:
            return self.MISSING_VALUE
        return self.data[self.CRITICALITY_KEY]

    def is_alive(self, ttl: int) -> bool:
        max_ttl = self.get_config_ttl(ttl)

        emitted_at = self.get_created_at()
        current = int(time())
        return (current - emitted_at) < max_ttl
