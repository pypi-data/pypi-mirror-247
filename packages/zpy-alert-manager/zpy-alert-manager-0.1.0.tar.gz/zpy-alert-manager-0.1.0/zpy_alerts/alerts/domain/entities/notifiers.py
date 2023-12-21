from abc import ABC, abstractmethod
from zpy_alerts.alerts.domain.entities.entities import AlertRawData
from zpy_alerts.alerts.domain.entities.delivery_result import NotifierResult


class AlertNotifier(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def emit(self, data: AlertRawData) -> NotifierResult:
        pass
