import multiprocessing
from functools import reduce

from src.parsers import parse
from src.reports import AvailableReportName, Report, report_factory


def build_report(files: list[str], report_name: AvailableReportName):
    with multiprocessing.Pool() as pool:
        args = [[file, report_name] for file in files]
        reports = pool.starmap(process_file, args)

    report = merge_reports(reports)
    report.print()


def process_file(file_name: str, report_name: AvailableReportName) -> Report:
    report_class = report_factory.get(report_name)
    report = report_class()

    with open(file_name, "r") as file:
        for line in file:
            record = parse(line.strip())
            if record and report.is_record_suitable(record):
                report.update(record)
    return report


def merge_reports(reports: list[Report]) -> Report:
    return reduce(lambda x, y: x.merge(y), reports)
