from zpy_alerts.alerts.domain.entities.filters import AlertFilter
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


class DenyOriginAlertFilter(AlertFilter):
    """
    Filter alert to deny specific origins
    """

    def __init__(self, deny: list[str]) -> None:
        super().__init__("DenyOriginAlertFilter")
        self.deny_origins = deny

    def verify(self, alert_data: AlertRawData) -> bool:
        return not alert_data.get_origin() in self.deny_origins
