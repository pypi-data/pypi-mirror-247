from typing import Optional, Callable
from zpy_alerts.alerts.domain.entities.filters import AlertFilter
from zpy_alerts.alerts.domain.constants.alert_types import AlertTypes
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


TTLValidator = Callable[[AlertRawData], bool]


class TTLAlertFilter(AlertFilter):
    """
    Alert filter to only allow valid ttl
    """

    def __init__(self, ttl: int = 300, ttl_validator: Optional[TTLValidator] = None) -> None:
        """Create ttl alert filter

        Args:
            ttl (int, optional): Max ttl in seconds to allow for emit alert. Defaults to 300.
            ttl_validator (Optional[TTLValidator], optional): Custom ttl validator. Defaults to None.
        """
        super().__init__("TTLAlertFilter")
        self.ttl_validator = ttl_validator
        self.default_ttl = ttl

    def verify(self, alert_data: AlertRawData) -> bool:
        if self.ttl_validator is not None:
            return self.ttl_validator(alert_data)
        return alert_data.is_alive(self.default_ttl)
