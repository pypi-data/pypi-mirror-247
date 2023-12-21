from zpy_alerts.alerts.domain.entities.filters import AlertFilter
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


class AllowOriginAlertFilter(AlertFilter):
    """
    Filter alert to allow specific origins
    """

    def __init__(self, allow: list[str]) -> None:
        super().__init__("AllowOriginAlertFilter")
        self.allow_origins = allow

    def verify(self, alert_data: AlertRawData) -> bool:
        return alert_data.get_origin() in self.allow_origins
