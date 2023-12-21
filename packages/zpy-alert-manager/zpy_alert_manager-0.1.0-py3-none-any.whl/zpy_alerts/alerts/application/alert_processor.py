from zpy_alerts.alerts.domain.entities.entities import AlertRawData
from zpy_alerts.alerts.domain.entities.delivery_result import DeliveryAlertResult
from ..domain.entities.filters import AlertFilter
from ..domain.entities.notifiers import AlertNotifier


class AlertProcessor:

    def __init__(
        self,
        notifiers: list[AlertNotifier],
        filters: list[AlertFilter]
    ) -> None:
        self.filters = filters
        self.notifiers = {x.name: x for x in notifiers}

    def execute(self, event: AlertRawData) -> DeliveryAlertResult:
        """Execute alert processor

        Args:
            event (AlertRawData): Alert raw event data
        """

        try:
            for filter in self.filters:
                if not filter.verify(event):
                    return DeliveryAlertResult.skip(f"Deny by filter: {filter.name}")

            results = self.__execute_notifiers(event)

            return DeliveryAlertResult.emit("Alert emitted", {
                'results': results
            })
        except Exception as e:
            print(e)
            return DeliveryAlertResult.fail(
                f"Fatal error occurred while processing alert: {event.get_alert_info()}",
                e
            )

    def __execute_notifiers(self, event: AlertRawData) -> list[str]:
        """Execute all notifiers for emit alerts

        Args:
            event (AlertRawData): Alert data to emit

        Returns:
            list[str]: Message result of all configured notifiers
        """
        return [self.__emit(self.notifiers[notifier], event) for notifier in self.notifiers.keys()]

    def __emit(self, notifier: AlertNotifier, event: AlertRawData) -> str:
        try:
            notifier.emit(event)
            return f"Alert emit successfully with {notifier.name} notifier."
        except Exception as e:
            print(e)
            return f"Fatal error ocurred when try to emit alert with notifier: {notifier.name}: {e}"
