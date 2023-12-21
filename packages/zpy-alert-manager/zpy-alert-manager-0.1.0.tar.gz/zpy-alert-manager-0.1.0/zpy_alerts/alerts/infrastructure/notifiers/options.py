from dataclasses import dataclass


@dataclass
class Options:
    channels: dict[str, dict]


@dataclass
class NotifierOptions:
    notifiers: dict[str, Options]
