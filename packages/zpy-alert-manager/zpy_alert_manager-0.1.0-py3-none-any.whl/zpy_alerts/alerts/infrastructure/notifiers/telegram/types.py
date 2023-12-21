from typing import Callable
from zpy_alerts.alerts.domain.entities.entities import AlertRawData


AlertContentRender = Callable[[AlertRawData, str], str]
