from zpy_alerts.alerts.domain.entities.filters import AlertFilter
from zpy_alerts.alerts.domain.constants.alert_types import CriticalityLevelAlert
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


class CriticalityAlertFilter(AlertFilter):
    """
    Filter to allow only configured criticality levels
    """

    def __init__(self, levels: list[str]) -> None:
        super().__init__("CriticalityAlertFilter")
        self.levels = levels

    def verify(self, alert_data: AlertRawData) -> bool:
        return alert_data.get_criticality_level() in self.levels
