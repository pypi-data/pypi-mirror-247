from dataclasses import dataclass


@dataclass
class ApiEventAlertData:
    request: dict
    response: dict
