from dataclasses import dataclass


@dataclass
class TelegramChannel:
    bid: str
    cid: str
    active: bool

    @staticmethod
    def of_dict(raw: dict) -> 'TelegramChannel':
        return TelegramChannel(**raw)
