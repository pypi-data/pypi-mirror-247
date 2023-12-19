"""
TS SDK v1 Bulk Upload example

Submits one or more reports from local files (txt, pdf)

Requirements
pip install trustar, pdfminer

Run
python bulk_upload.py --dir ./files_to_upload_dir/ --ts_conf ./trustar_api.conf
"""
# ! /usr/local/bin/python3

import argparse
import os
import time
import json
import pdfminer.pdfinterp

from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

from trustar import log, Report, TruStar


logger = log.get_logger(__name__)


def extract_pdf(file_name):
    """
    Extract text from a pdf file
    :param file_name path to pdf to read
    :return text from pdf
    """
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    sio = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec="utf-8", laparams=laparams)
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)

    # Extract text from pdf file
    with open(file_name, 'rb') as fp:
        for page in PDFPage.get_pages(fp, maxpages=20):
            interpreter.process_page(page)

    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text


def process_file(source_file):
    """
    Extract text from a file (pdf, txt, eml, csv, json)
    :param source_file path to file to read
    :return text from file
    """
    txt = ""
    if source_file.endswith(('.pdf', '.PDF')):
        txt = extract_pdf(source_file)
    elif source_file.endswith(('.txt', '.eml', '.csv', '.json')):
        with open(source_file, 'r') as f:
            txt = f.read()
    else:
        logger.info(f"Unsupported file extension for file {source_file}")

    return txt


def main():
    """
    Submit one or more reports from local files (txt, pdf)

    Requirements
    pip install trustar, pdfminer

    Run
    python bulk_upload.py --dir ./files_to_upload_dir/ --ts_conf ./trustar_api.conf
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=(
                                         'Submit one or more reports from local files (txt, pdf, docx, etc) '
                                         'in a directory\n\n'
                                         'Example:\n'
                                         'python bulk_upload.py --dir ./sample_reports --ts_conf ./trustar.conf'))
    parser.add_argument('--dir', '-d', help='Path containing report files', required=True)
    parser.add_argument('--ts_config', '-c', help='Path containing trustar api config', nargs='?', default="./trustar.conf")
    parser.add_argument('-i', '--ignore', dest='ignore', action='store_true',
                        help='Ignore history and resubmit already procesed files')

    args = parser.parse_args()
    source_report_dir = args.dir

    ts_config = args.ts_config
    ts = TruStar(config_file=ts_config)

    # process all files in directory
    logger.info(f"Processing each source file in {source_report_dir} as a TruSTAR Incident Report")

    processed_files = set()

    processed_files_file = os.path.join(source_report_dir, "processed_files.log")
    if os.path.isfile(processed_files_file) and not args.ignore:
        processed_files = set(line.strip() for line in open(processed_files_file))

    skipped_files_file = os.path.join(source_report_dir, "skipped_files.log")

    with open(processed_files_file, 'a', 0) as pf:
        for (dirpath, dirnames, filenames) in os.walk(source_report_dir):
            for source_file in filenames:

                if source_file in ("processed_files.log", "skipped_files.log"):
                    continue

                if source_file in processed_files:
                    logger.debug(f"File {source_file} was already processed. Skipping...")
                    continue

                logger.info(f"Processing source file {source_file}")
                try:
                    path = os.path.join(source_report_dir, source_file)
                    report_body = process_file(path)
                    if not report_body:
                        logger.debug(f"File {source_file} ignored for no data")
                        raise

                    logger.info(f"Report {report_body}")
                    try:
                        report = Report(title=f"ENCLAVE: {source_file}",
                                        body=report_body,
                                        is_enclave=True,
                                        enclave_ids=ts.enclave_ids)
                        report = ts.submit_report(report)
                        logger.info(f"Successfully submitted TruSTAR Report as Incident Report ID {report.id}")
                        pf.write(f"{source_file}\n")

                        if report.indicators:
                            print(f"Extracted the following indicators: {json.dumps([ioc.to_dict() for ioc in report.indicators], indent=2)}")
                        else:
                            print(f"No indicators returned from report id {report.id}")
                    except Exception as e:
                        if '413' in e.message:
                            logger.warning("Could not submit file {source_file}. Contains more indicators than currently supported.")
                        else:
                            raise

                except Exception as e:
                    logger.exception(f"Problem with file {source_file}, exception:{e}")
                    with open(skipped_files_file, 'w', 0) as sf:
                        sf.write(f"{source_file}\n")
                    continue

                time.sleep(2)


if __name__ == '__main__':
    # Executes main
    main()
