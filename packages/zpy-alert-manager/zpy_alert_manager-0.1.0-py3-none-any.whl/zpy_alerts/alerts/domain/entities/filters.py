from abc import ABC, abstractmethod
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


class AlertFilter(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def verify(self, alert_data: AlertRawData) -> bool:
        pass
