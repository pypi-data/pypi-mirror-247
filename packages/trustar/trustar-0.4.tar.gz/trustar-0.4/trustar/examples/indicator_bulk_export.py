"""
TS SDK v1 Bulk Export example for Indicators Bulk Export

This script will initiate a bulk export of all indicator metadata for indicators
that contain google.com and save them to a local file.
"""
# ! /usr/local/bin/python3

from time import sleep

from trustar import log, TruStar

# initialize SDK
ts = TruStar()

# initialize logger
logger = log.get_logger(__name__)



# This script will initiate a bulk export of all indicator metadata for
# indicators that contain google.com and save them to a local file.
guid = ts.initiate_indicator_metadata_export('google.com')
logger.info(f"Job initiated - {guid}")

sleep(10)
status = ts.get_indicator_metadata_export_status(guid)
logger.info(f"Status = {status}")

# Loop until the status is either ERROR or COMPLETE
while status not in ("ERROR", "CANCELED", "COMPLETE"):
    sleep(10)
    status = ts.get_indicator_metadata_export_status(guid)
    logger.info(f"Status = {status}")

if status == "ERROR":
    logger.error("Job failed")
elif status == "CANCELED":
    logger.error("Job was canceled")
else:
    logger.info(f"Saving export to {guid}.csv")
    ts.download_indicator_metadata_export(guid, f"{guid}.csv")
    logger.info("Export complete!")
