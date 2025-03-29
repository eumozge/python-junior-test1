import argparse

from src.bulders import build_report
from src.reports import report_factory, AvailableReportName
from src.validators import FileExistValidator

parser = argparse.ArgumentParser(
    description="Build analytics reports based on application logs."
)
parser.add_argument(
    "files",
    nargs="+",
    action=FileExistValidator,
    help="list of log files as: file1.log file2.log ...",
)
parser.add_argument(
    "--report",
    choices=report_factory.registered_reports,
    required=True,
    help="report name",
)


def main(files: list[str], report_name: str):
    build_report(files=files, report_name=AvailableReportName(report_name))


if __name__ == "__main__":
    args = parser.parse_args()
    main(files=args.files, report_name=args.report)
