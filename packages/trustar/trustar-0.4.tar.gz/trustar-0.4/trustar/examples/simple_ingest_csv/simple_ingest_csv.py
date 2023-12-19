"""
TS SDK v1 Simple Ingest CSV example
"""
# ! /usr/local/bin/python3

import csv

from trustar import log, Report, TruStar


logger = log.get_logger(__name__)


# mapping of CSV column names to report fields
MAPPING = {
    "title": "name",
    "body": "content",
    "external_id": "id"
}

CSV_PATH = "reports.csv"

# initialize SDK
ts = TruStar()

# Reads reports from a CSV and submits them to TruSTAR API 1.3
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    # iterate over rows
    for row in reader:

        # define method to get report field from CSV row
        def get_field(field):
            return row.get(MAPPING.get(field))

        # construct report from CSV row
        report = Report(title=get_field('title'),
                        body=get_field('body'),
                        external_id=get_field('external_id'),
                        is_enclave=True,
                        enclave_ids=ts.enclave_ids)

        # submit report
        ts.submit_report(report)

        logger.info("Submitted report: %s", report)
