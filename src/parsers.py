import dataclasses
from typing import Optional


@dataclasses.dataclass(slots=True)
class LogRecord:
    raw: str
    timestamp: str
    log_level: str
    record_type: str
    request_handler: Optional[str]
    request_method: Optional[str]
    status_code: Optional[int]


class LogRecordParser:
    def __init__(self, raw: str):
        self.raw = raw

    def parse(self) -> Optional[LogRecord]:
        pass


def parse(raw: str) -> Optional[LogRecord]:
    return LogRecordParser(raw).parse()
