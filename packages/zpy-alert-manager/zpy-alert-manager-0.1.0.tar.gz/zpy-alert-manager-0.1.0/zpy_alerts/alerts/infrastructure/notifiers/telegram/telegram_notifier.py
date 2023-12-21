from zpy_alerts.alerts.domain.entities.notifiers import AlertNotifier
from zpy_alerts.alerts.infrastructure.notifiers.options import Options
from zpy_alerts.alerts.infrastructure.notifiers.telegram.objects import TelegramChannel
from typing import Optional
from zpy_alerts.alerts.infrastructure.notifiers.telegram.types import AlertContentRender
from zpy.utils.values import if_null_get
from zpy.utils.http_client import ZHttp
from zpy_alerts.alerts.infrastructure.notifiers.telegram.telegram_renders import wrap_message, telegram_renders
from zpy_alerts.alerts.domain.entities.entities import AlertRawData
from zpy_alerts.alerts.domain.entities.delivery_result import NotifierResult


class TelegramNotifier(AlertNotifier):
    BOT_API = 'https://api.telegram.org/bot'

    def __init__(
            self,
            options: Options,
            renders: Optional[dict[str, AlertContentRender]] = None,
            bot_api: Optional[str] = None
    ) -> None:
        super().__init__('telegram')
        self.api = if_null_get(bot_api, self.BOT_API)
        self.options = options
        self.channels: dict[str, TelegramChannel] = {
            k: TelegramChannel.of_dict(options.channels[k]) for k in options.channels.keys()
        }
        self.renders = if_null_get(renders, telegram_renders)

    def emit(self, data: AlertRawData) -> NotifierResult:
        channels = data.get_config_channels_of_notifier(self.name)
        result = {name: self.__emit_to(data, name) for name in channels}
        return NotifierResult(result)

    def __emit_to(self, data: AlertRawData, name: str):
        channel_config = self.channels.get(name, None)

        if not channel_config:
            return f"Alert cant be emitted to {name} channel because not exist or missing config."

        api = f'{self.api}{channel_config.bid}'
        alert_type = data.get_type()
        descriptor = self.renders.get(alert_type)
        if not descriptor:
            return f'Alert cant be emitted to {name} because doesnt exist render for alert type'

        presentable_content = wrap_message(descriptor(data, alert_type))

        result = ZHttp.post('{0}/sendMessage?chat_id={1}&parse_mode=html&text={2}'
                            .format(api, channel_config.cid, presentable_content))

        return f"{alert_type} alert emitted successfully with Telegram bot to {name} channel."
