from zpy_alerts.alerts.domain.entities.filters import AlertFilter
from zpy_alerts.alerts.domain.constants.alert_types import AlertTypes
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


class TypeAlertFilter(AlertFilter):
    """
    Alert filter to only allow configured types
    """

    def __init__(self, types: list[str]) -> None:
        super().__init__("TypeAlertFilter")
        self.raw_types = types

    def verify(self, alert_data: AlertRawData) -> bool:
        return alert_data.get_type() in self.raw_types
