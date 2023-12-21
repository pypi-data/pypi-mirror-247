from enum import Enum
from typing import List


class CriticalityLevelAlert(str, Enum):
    """Criticality level of alerts
    """
    CRITICAL = 'CRITICAL'
    WARN = 'WARN'
    INFO = 'INFO'

    @staticmethod
    def all_values() -> list[str]:
        return [v.value for v in CriticalityLevelAlert]

    @staticmethod
    def all() -> list['CriticalityLevelAlert']:
        return [v for v in CriticalityLevelAlert]


class AlertTypes(Enum):
    """
        Alert types
    """
    API_EVENT = 'API_EVENT'
    SQS_EVENT = 'SQS_EVENT'
    API_CALL = 'API_CALL'
    MESSAGE = 'MESSAGE'

    @staticmethod
    def all():
        return [
            AlertTypes.API_CALL,
            AlertTypes.API_EVENT,
            AlertTypes.SQS_EVENT,
            AlertTypes.MESSAGE
        ]

    @staticmethod
    def all_values() -> list[str]:
        return [v.value for v in AlertTypes]