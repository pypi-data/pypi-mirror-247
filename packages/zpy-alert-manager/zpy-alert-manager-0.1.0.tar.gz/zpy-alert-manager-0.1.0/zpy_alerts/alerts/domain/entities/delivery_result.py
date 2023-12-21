from dataclasses import dataclass
from typing import Optional


@dataclass
class DeliveryAlertResult:
    delivery: bool
    message: Optional[str]
    error: Optional[Exception]
    skipped: Optional[bool]
    skipped_reason: Optional[str]
    data: Optional[dict]

    @classmethod
    def skip(cls, reason: str):
        return cls(False, None, None, True, reason, None)

    @classmethod
    def fail(cls, message: str, e: Exception):
        return cls(False, message, e, False, None, None)

    @classmethod
    def emit(cls, message: str, result: dict):
        return cls(True, message, None, False, None, result)


@dataclass
class NotifierResult:
    channels: Optional[dict]
