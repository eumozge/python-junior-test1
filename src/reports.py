from __future__ import annotations

import abc
from collections import defaultdict
from enum import StrEnum

from src.parsers import LogRecord


class AvailableReportName(StrEnum):
    HANDLERS = "handlers"


class Report(abc.ABC):
    def __init__(self):
        self.metrics = {}

    @abc.abstractmethod
    def is_record_suitable(self, record: LogRecord) -> bool:
        """
        Some log records are not taken into report, for example:
        the report should be built based only on django.requests log records.
        """

    @abc.abstractmethod
    def update(self, record: LogRecord):
        """
        Updating report metrics based on data from each subsequent record.
        """

    @abc.abstractmethod
    def merge(self, other: Report) -> Report:
        """
        Several reports can be generated from several files,
        they need to be combined into one for printing.
        """

    @abc.abstractmethod
    def print(self):
        pass


class ReportFactory:
    def __init__(self):
        self.registry = {}

    @property
    def registered_reports(self):
        return [report.value for report in self.registry.keys()]

    def register(self, report_name: AvailableReportName):
        def decorator(target_report_class: Report) -> Report:
            self.registry[report_name] = target_report_class
            return target_report_class

        return decorator

    def get(self, report_name: AvailableReportName) -> Report:
        return self.registry[report_name]


report_factory = ReportFactory()


@report_factory.register(AvailableReportName.HANDLERS)
class HandlerReport(Report):
    @property
    def handlers(self):
        return self.metrics.setdefault("handlers", {})

    @property
    def summary(self):
        return self.metrics.setdefault("summary", defaultdict(int))

    def is_record_suitable(self, record: LogRecord) -> bool:
        return record.record_type == "django.requests"

    def update(self, record: LogRecord):
        handler = self.handlers.setdefault(record.request_handler, defaultdict(int))
        handler[record.log_level] += 1
        self.summary[record.log_level] += 1

    def merge(self, other: Report) -> Report:
        pass

    def print(self):
        pass
