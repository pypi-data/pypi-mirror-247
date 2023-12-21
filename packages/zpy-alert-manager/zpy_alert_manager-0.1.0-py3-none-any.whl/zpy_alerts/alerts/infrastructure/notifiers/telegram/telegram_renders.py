# Created by Noé Cruz | Zurckz 22 at 26/03/2022
from zpy.utils.dates import apply_tz
from zpy_alerts.alerts.domain.constants.alert_types import AlertTypes, CriticalityLevelAlert
from zpy_alerts.alerts.infrastructure.notifiers.telegram.types import AlertContentRender
from typing import Dict
from datetime import datetime
from enum import Enum
import re
from zpy_alerts.alerts.domain.entities.entities import AlertRawData

icons = {
    AlertTypes.API_EVENT.value: u'\U0001F310',
    AlertTypes.API_CALL.value: u'\U0001F4E1',
    AlertTypes.SQS_EVENT.value: u'\U0001F500',
    AlertTypes.MESSAGE.value: u'\U0001F4E8',
    CriticalityLevelAlert.CRITICAL.value: u'\U0001F534 - \U0001F621',
    CriticalityLevelAlert.WARN.value: u'\U000026A0 - \U0001F61F',
    CriticalityLevelAlert.INFO.value: u'\U00002139 - \U0001F642'
}


class PlaceHolders(Enum):
    ALARM_ICON = "@alarm_i", u'\U0001F6A8'
    METRIC_TYPE_ICON = "@type_i", u'\U0001F631'
    METRIC = "@metric_type", '-'
    ORIGIN_ICON = "@origin_i", u'\U000026A1'
    ORIGIN = "@origin", '-'
    CRITICALITY_ICON = "@criticality_i", u'\U0001F6A9'
    CRITICALITY = "@criticality", '-'
    EMITTED_ICON = "@emitted_i", u'\U0001F563'
    EMITTED = "@emitted", '-'
    REQUEST_ID = "@request_id", '-'
    RESOURCE = "@resource", '-'
    PATH = "@path", '-'
    METHOD = "@method", '-'
    STATUS = "@status", '-'
    RESPONSE = "@response", '-'
    WARN_ICON = "@warn_i", u'\U000026A0'
    VERSION = "@version", '1.0.0'
    REQUEST = '@request', '-'
    MESSAGE = '@message', '-'
    RECORD_SRC = '@record_src', '-'

    @staticmethod
    def new() -> Dict[str, str]:
        return {p.value[0]: p.value[1] for p in PlaceHolders}

    @staticmethod
    def new_render(type: str, level: str) -> Dict[str, str]:
        return {p.value[0]: p.value[1] for p in PlaceHolders}

    @staticmethod
    def update(current: dict, mask, value):
        current.update({mask.mask: value})

    @property
    def mask(self):
        return self.value[0]


telegram_templates = {
    "HEADER_TEMPLATE": """<b><strong>@alarm_i New Alert @alarm_i</strong></b>\n
<b>Type: @type_i \n <code>@metric_type</code></b>\n
<b>Origin: @origin_i\n <code>@origin</code></b>\n
<b>Criticality: @criticality_i\n <code>@criticality</code></b>\n
<b>Emitted At: @emitted_i\n <code>@emitted</code></b>\n""",
    "API_EVENT": """\n<b>Request ID:\n <code>@request_id</code></b>\n
<b>Resource:\n <code>@resource</code></b>\n
<b>Path:\n <code>@path</code></b>\n
<b>Method:\n <code>@method</code></b>\n
<b>Status Code:\n <code>@status</code></b>\n
<b>Raw Response:</b>\n
<pre>@response</pre>""",
    "SQS_EVENT": """\n<b>Messages IDs:\n <code>@request_id</code></b>\n
<b>Record origin:\n <code>@record_src</code></b>\n
<b>Message:\n <code>@message</code></b>\n
<b>Raw Response:</b>\n
<pre>@response</pre>""",
    "API_CALL": """<b>\nURL:\n <code>@path</code></b>\n
<b>Status:\n <code>@status</code></b>\n
<b>Raw Response:</b>\n
<pre>@response</pre>""",
    "MESSAGE": """\n<b>Message:</b>\n
<pre>@message</pre>
""",
    "FOOTER": "\n\n\t<b>@warn_i End of Alert</b> @warn_i\n",
    "BOT_TAG": "\n<tg-spoiler><b>BotNotifier @version</b> ~ <i>Built by Noé Cruz | Zurckz</i></tg-spoiler>"
}


def render_template(place_holders: Dict[str, str], template: str):
    rep = dict((re.escape(k), v) for k, v in place_holders.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], template)


def initialize_placeholders(metric_type: str, origin: str, criticality: str, emitted_at: str) -> dict:
    placeholders = PlaceHolders.new()
    placeholders[PlaceHolders.METRIC_TYPE_ICON.mask] = icons.get(
        metric_type, u'\U0001F4E2')
    placeholders[PlaceHolders.CRITICALITY_ICON.mask] = icons.get(
        criticality, u'\U000026AA - \U0001F610')
    placeholders[PlaceHolders.METRIC.mask] = metric_type
    placeholders[PlaceHolders.ORIGIN.mask] = origin
    placeholders[PlaceHolders.CRITICALITY.mask] = criticality
    placeholders[PlaceHolders.EMITTED.mask] = emitted_at
    return placeholders


def get_telegram_template(metric_type: str) -> str:
    template = telegram_templates.get(metric_type, None)
    if not template:
        raise ValueError('Template type cant be null')
    header = telegram_templates.get("HEADER_TEMPLATE")
    footer = telegram_templates.get("FOOTER")
    return f'{header}{template}{footer}'


def wrap_message(message: str) -> str:
    placeholders = PlaceHolders.new()
    footer = telegram_templates.get("BOT_TAG")
    return render_template(placeholders, f'{message}{footer}')


def api_event_descriptor(raw_data: AlertRawData, metric_type: str) -> str:
    """
    API EVENT descriptor for Telegram notifier.
    """
    data = raw_data.data
    template = get_telegram_template(metric_type)

    emitted_at = apply_tz(datetime.fromtimestamp(
        int(data.get('created_at', datetime.now().timestamp()))))
    metric_data: dict = data.get('data', {})
    metric_request: dict = metric_data.get('request', {})
    metric_response: dict = metric_data.get('response', {})
    placeholders = initialize_placeholders(metric_type, data.get('origin', '-'), data.get('criticality', '-'),
                                           emitted_at.strftime("%d/%m/%Y, %H:%M:%S"))

    placeholders[PlaceHolders.REQUEST_ID.mask] = raw_data.get_context_request_id()
    placeholders[PlaceHolders.RESOURCE.mask] = metric_request.get(
        'resource', '-')
    placeholders[PlaceHolders.PATH.mask] = metric_request.get('path', '-')
    placeholders[PlaceHolders.METHOD.mask] = metric_request.get(
        'httpMethod', '-')
    placeholders[PlaceHolders.STATUS.mask] = str(
        metric_response.get('statusCode', '-'))
    placeholders[PlaceHolders.RESPONSE.mask] = metric_response.get('body', '-')

    return render_template(placeholders, template)


def sqs_event_descriptor(raw_data: AlertRawData, metric_type: str) -> str:
    """
    SQS EVENT descriptor for Telegram notifier.
    """
    data = raw_data.data
    template = get_telegram_template(metric_type)
    emitted_at = apply_tz(datetime.fromtimestamp(
        int(data.get('created_at', datetime.now().timestamp()))))
    metric_data: dict = data.get('data', {})

    placeholders = initialize_placeholders(metric_type, data.get('origin', '-'), data.get('criticality', '-'),
                                           emitted_at.strftime("%d/%m/%Y, %H:%M:%S"))

    final_records = []
    if 'record' in metric_data:
        final_records.append(metric_data.get('record'))

    if 'Records' in metric_data:
        final_records.extend(metric_data.get('Records', []))

    if len(final_records) > 0:
        src = final_records[0].get('attributes', {}).get(
            'SenderId', '-').split(":")
        if len(src) >= 1:
            placeholders[PlaceHolders.RECORD_SRC.mask] = src[1]

    messages_ids = ", ".join([r.get('messageId', '-') for r in final_records])
    placeholders[PlaceHolders.REQUEST_ID.mask] = messages_ids
    placeholders[PlaceHolders.RESPONSE.mask] = metric_data.get('result', '-')
    placeholders[PlaceHolders.MESSAGE.mask] = metric_data.get('message', '-')

    return render_template(placeholders, template)


def api_call_event_descriptor(raw_data: AlertRawData, metric_type: str) -> str:
    """
    SQS EVENT descriptor for Telegram notifier.
    """
    data = raw_data.data
    template = get_telegram_template(metric_type)
    emitted_at = apply_tz(datetime.fromtimestamp(
        int(data.get('created_at', datetime.now().timestamp()))))
    metric_data: dict = data.get('data', {})

    placeholders = initialize_placeholders(metric_type, data.get('origin', '-'), data.get('criticality', '-'),
                                           emitted_at.strftime("%d/%m/%Y, %H:%M:%S"))

    raw_response = metric_data.get('response', '-')
    if isinstance(raw_response, dict):
        raw_response = f"{raw_response}"

    placeholders[PlaceHolders.PATH.mask] = metric_data.get(
        'url', '-').replace("#", "")
    placeholders[PlaceHolders.STATUS.mask] = str(
        metric_data.get('status', '-'))
    placeholders[PlaceHolders.RESPONSE.mask] = raw_response.replace('#', '')

    return render_template(placeholders, template)


def message_event_descriptor(raw_data: AlertRawData, metric_type: str) -> str:
    """
    SQS EVENT descriptor for Telegram notifier.
    """
    data = raw_data.data
    template = get_telegram_template(metric_type)
    emitted_at = apply_tz(datetime.fromtimestamp(
        int(data.get('created_at', datetime.now().timestamp()))))
    metric_data: dict = data.get('data', {})

    placeholders = initialize_placeholders(metric_type, data.get('origin', '-'), data.get('criticality', '-'),
                                           emitted_at.strftime("%d/%m/%Y, %H:%M:%S"))

    placeholders[PlaceHolders.MESSAGE.mask] = metric_data.get('content', '-')

    return render_template(placeholders, template)


telegram_renders: Dict[str, AlertContentRender] = {
    AlertTypes.API_EVENT.value: api_event_descriptor,
    AlertTypes.SQS_EVENT.value: sqs_event_descriptor,
    AlertTypes.API_CALL.value: api_call_event_descriptor,
    AlertTypes.MESSAGE.value: message_event_descriptor,
}
