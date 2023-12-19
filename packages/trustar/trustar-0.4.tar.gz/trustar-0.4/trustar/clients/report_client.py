"""
Implements TS API v1.3 Reports protocols
"""
# ! /usr/local/bin/python3

# external imports
import json
from datetime import datetime
import functools

# internal imports
from clients.api_client import APIClient
from log import get_logger
from models import (
    DistributionType, IdType, NumberedPage, Pagination, RedactedReport, Report,
    ReportsParameters, TSPaginationKeys, TSReportParameterKeys,
)
from protocols.reports_protocol import ReportsAPI


logger = get_logger(__name__)


class ReportClient(ReportsAPI):
    """
    Class which implements TruSTAR API v1.3 Reports protocols

    Reports: https://docs.trustar.co/api/v13/reports/index.html
    """

    def __init__(self, api_client: APIClient=None):
        """
        Constructs a |PhishingTriageClient| object.
        """
        self._api_client = api_client

    def submit_report(self, reports_params: ReportsParameters=None):
        """
        Submits a Report

        * If `report.is_enclave` is `True`, then the report will be submitted to
            the enclaves identified by `report.enclaves`; if that field is `None`
            it defaults to 'default'
        * If `report.time_began` is `None`, then the current time will be used

        :param report: The |Report| object to be submitted

        :return: The |Report| object that was submitted with the `id` field
            updated based on values from the response

        Example:
        >>> report = Report(title="Suspicious Activity",
        >>>                 body="We have been receiving suspicious requests from 169.178.68.63",
        >>>                 enclave_ids=["602d4795-31cd-44f9-a85d-f33cb869145a"])
        >>> report = ts.submit_report(report)
        >>> print(report.id)
        ac6a0d17-7350-4410-bc57-9699521db992
        >>> print(report.title)
        Suspicious Activity
        """
        report = reports_params.report
        # make distribution type default to "enclave"
        if report.is_enclave is None:
            report.is_enclave = True

        if report.enclave_ids is None:
            # Use 'default' enclave_ids if distribution type is ENCLAVE
            # If distribution type is COMMUNITY, API still expects non-null
            # list of enclaves
            report.enclave_ids = ['default'] if report.is_enclave else []

        if report.is_enclave and not report.enclave_ids:
            empty_enclave_ids_msg = ("Cannot submit a report of distribution type "
                                     "'ENCLAVE' with an empty set of enclaves.")
            raise ValueError(empty_enclave_ids_msg)

        # default time began is current time
        if report.time_began is None:
            report.set_time_began(datetime.now())

        resp = self._api_client.post("reports",
                                     data=json.dumps(report.to_dict()),
                                     timeout=60)

        # get report id from response body
        report_id = resp.content

        if isinstance(report_id, bytes):
            report_id = report_id.decode("utf-8")

        report.id = report_id

        return report

    def update_report(self, reports_params: ReportsParameters=None):
        """
        Updates the report identified by the `report.id` field; if this field does
        not exist, then `report.external_id` will be used if it exists. Any
        other fields on `report` that are not `None` will overwrite values on
        the report in TS's systems. Any fields that are `None` will simply be
        ignored; their values will be unchanged

        :param report: A |Report| object with the updated values

        :return: The |Report| object

        Example:
        >>> report = ts.get_report_details(report_id)
        >>> print(report.title)
        Old Title
        >>> report.title = "Changed title"
        >>> updated_report = ts.update_report(report)
        >>> print(updated_report.title)
        Changed Title
        """
        report = reports_params.report
        # default to interal ID type if ID field is present
        if report.id:
            id_type = IdType.INTERNAL
            report_id = report.id
        # if no ID field is present, but external ID field is, default to external ID type
        elif report.external_id:
            id_type = IdType.EXTERNAL
            report_id = report.external_id
        # if no ID fields exist, raise exception
        else:
            raise AttributeError("Cannot update report without ID: either "
                                 "internal or external")

        # not allowed to update value of 'reportId', so remove it
        updated_report = {k: v for k, v in report.to_dict().items()
                          if k != TSReportParameterKeys.REPORT_ID.value}
        params = {TSReportParameterKeys.ID_TYPE.value: id_type}

        self._api_client.put(f"reports/{report_id}",
                             params=params,
                             data=json.dumps(updated_report))

        return report

    def upsert_report(self, reports_params: ReportsParameters=None):
        """
        Submits a new incident report and receive the ID it has been assigned in
        TS systems, or update and existing report using and existing ID.
        This endpoint will act as submit or update reports endpoints

        :param report: A |Report| object

        :return: The |Report| guid value

        Example:
        >>> report = Report(title="Notable Activity",
        >>>                 body="We have been receiving dubious requests from 178.68.169.63",
        >>>                 enclave_ids=["f33cb869145a-44f9-a85d-31cd-602d4795"])
        >>> report_guid = ts.upsert_report(report)
        >>> print(report_guid)
        9699521db992-4410-bc57-7350-ac6a0d17
        """
        params = {
            TSReportParameterKeys.ID_TYPE.value: reports_params.id_type,
            TSReportParameterKeys.MODE.value: reports_params.mode or "OVERRIDE",
        }

        guid = self._api_client.post("reports/upsert",
                                     params=params,
                                     data=json.dumps(reports_params.report.to_dict()))

        return guid

    def get_report_details(self, reports_params: ReportsParameters=None):
        """
        Retrieves a report by its ID. Internal and external IDs are both allowed

        :param str report_id: The ID of the incident report
        :param str id_type: Indicates whether ID is internal or external

        :return: The retrieved |Report| object

        Example:
        >>> report = ts.get_report_details("1a09f14b-ef8c-443f-b082-9643071c522a")
        >>> print(report)
        {
          "id": "1a09f14b-ef8c-443f-b082-9643071c522a",
          "created": 1515571633505,
          "updated": 1515620420062,
          "reportBody": "Employee reported suspect email. We had multiple reports overnight...",
          "title": "Phishing Incident",
          "enclaveIds": [
            "ac6a0d17-7350-4410-bc57-9699521db992"
          ],
          "distributionType": "ENCLAVE",
          "timeBegan": 1479941278000
        }
        """
        params = {TSReportParameterKeys.ID_TYPE.value: reports_params.id_type}

        resp = self._api_client.get(f"reports/{reports_params.report_id}",
                                    params=params)

        return Report.from_dict(resp.json())

    def delete_report(self, reports_params: ReportsParameters=None):
        """
        Deletes the report with the given ID

        :param report_id: The ID of the report to delete
        :param id_type: Indicates whether the ID is internal or external

        :return: The response object

        Example:
        >>> response = ts.delete_report("4d1fcaee-5009-4620-b239-2b22c3992b80")
        """
        params = {TSReportParameterKeys.ID_TYPE.value: reports_params.id_type}

        self._api_client.delete(f"reports/{reports_params.report_id}", params=params)

    def copy_report(self, reports_params: ReportsParameters=None):
        """
        Copies a report to another enclave. All properties of the report, including
        tags, will be copied. A reference to the original report will still be stored
        on the child, allowing the system to track the relationship between the
        original report and copies made from it

        If the `from_provided_submission` parameter is `True`, then edits can be
        applied to the copied report. This is useful in cases where the body or title
        must be redacted first, or the list of tags needs to be altered for the copy. 
        In this case, a |Report| object and a list of tag names must be provided,
        which will fill out the copied report. A reference to the original report
        will still be stored on the copy
        **NOTE:** Partial edits are not allowed.  ALL fields must be filled out
        on this object, and the fields from the original report will completely ignored

        :param str report_id: the ID of the report to copy
        :param str dest_enclave_id: the ID of the enclave to copy the report to
        :param boolean from_provided_submission: whether to apply edits from a
            supplied report object and list of tags
        :param Report report: (required if `from_provided_submission` is `True`) a
            report object containing an edited version to use as the copy. This
            allows information to be redacted, or other arbitrary edits to be made
            to the copied version
            **NOTE:** Partial edits are not allowed.  ALL fields must be filled
            out on this object, and the fields from the original report will
            completely ignored
        :param list(str) tags: (required if `from_provided_submission` is `True`) a
            list of tags to use if `from_provided_submission` is `True`.
            **NOTE:** if `from_provided_submission` is `True`, the tags from the
            source report will be completely ignored, and this list of tags will
            be used instead. MUST be provided if `from_provided_submission` is `True`

        :return: the ID of the newly-created copy
        """
        body = None
        params = {
            TSReportParameterKeys.DEST_ENCLAVE_ID.value: reports_params.dest_enclave_id,
            TSReportParameterKeys.FROM_SUBMISSION.value: reports_params.from_provided_submission
        }

        # determine if edits are being made to the copy
        if reports_params.from_provided_submission:
            # ensure an edited version of the report has been provided
            if not reports_params.report:
                raise AttributeError("Cannot copy from provided submission "
                                     "without providing a report object")
            # ensure an edited list of tags has been provided
            if not reports_params.tags:
                raise AttributeError("Cannot copy from provided submission "
                                     "without providing a list of tags")

            # form the JSON dictionary of the report
            body = reports_params.report.to_dict()
            # add the list of tags to the JSON
            # NOTE: this field on the report object cannot be used in other
            # endpoints on this API version
            body[TSReportParameterKeys.TAGS.value] = reports_params.tags

        response = self._api_client.post(f"reports/copy/{reports_params.report_id}",
                                         params=params,
                                         data=json.dumps(body))

        return response.json().get(TSReportParameterKeys.ID.value)

    def move_report(self, reports_params: ReportsParameters=None):
        """
        Move a report from one enclave to another
        **NOTE:** All tags will be moved, as well

        :param report_id: the ID of the report to move
        :param dest_enclave_id: the ID of the enclave to move the report to

        :return: the ID of the report
        """
        params = {TSReportParameterKeys.DEST_ENCLAVE_ID.value: reports_params.dest_enclave_id}

        response = self._api_client.post(f"reports/move/{reports_params.report_id}",
                                         params=params)

        return response.json().get(TSReportParameterKeys.ID.value)

    def get_correlated_reports(self,
                               reports_params: ReportsParameters=None,
                               page_number=None,
                               page_size=None
                               ):
        """
        Uses the |get_correlated_reports_page| method to create a generator that
        returns each successive report

        :param indicators: A list of indicator values to retrieve correlated reports for
        :param enclave_ids: The enclaves to search in
        :param is_enclave: Whether to search enclave reports or community reports
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: The generator
        """
        correlated_reports_page_gen = self._get_correlated_reports_page_generator(
            reports_params=reports_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=correlated_reports_page_gen)

    def search_reports(self,
                       reports_params: ReportsParameters=None,
                       page_number=None,
                       page_size=None
                       ):
        """
        Uses the |search_reports_page| method to create a generator that returns
        each successive report

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters
        :param list(str) enclave_ids: list of enclave ids used to restrict reports
            to specific enclaves (optional - by default reports from all of user's
            enclaves are returned)
        :param int from_time: start of time window in milliseconds since epoch (optional)
        :param int to_time: end of time window in milliseconds since epoch (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter reports by.
            Only reports containing ALL of these tags will be returned (optional)
        :param list(str) excluded_tags: Reports containing ANY of these tags will
            be excluded from the results
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: The generator of Report objects
        **NOTE**: the `body` attributes of these reports will be `None`
        """
        search_report_page_gen = self._search_reports_page_generator(
            reports_params=reports_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=search_report_page_gen)

    def redact_report(self, reports_params: ReportsParameters=None):
        """
        Redacts a report's title and body

        :param str title: The title of the report to apply redaction to
        :param str report_body: The body of the report to apply redaction to

        :return: A |RedactedReport| object
        """
        body = {
            TSReportParameterKeys.TITLE.value: reports_params.title,
            TSReportParameterKeys.REPORT_BODY.value: reports_params.report_body
        }

        resp = self._api_client.post("redaction/report",
                                     data=json.dumps(body))

        return RedactedReport.from_dict(resp.json())

    def get_report_status(self, reports_params: ReportsParameters=None):
        """
        Finds the processing status of a report

        :param report: A |Report| or a str object

        :return: A dict

        Example result:
        {
            "id": "3f8824de-7858-4e07-b6d5-f02d020ee675",
            "status": "SUBMISSION_PROCESSING",
            "errorMessage": ""
        }

        The possible status values for a report are:
        * SUBMISSION_PROCESSING,
        * SUBMISSION_SUCCESS,
        * SUBMISSION_FAILURE,
        * UNKNOWN

        A report can have an UNKNOWN processing status if the report
        has not begun processing or if it is an older report
        that has not been recently updated.

        >>> report = "fcda196b-eb30-4b59-83b8-a25ab6d70d17"
        >>> result = ts.get_report_status(report)
        >>> result['status']
        "SUBMISSION_SUCCESS"
        """
        report = reports_params.report
        if isinstance(report, Report):
            lookup = report.id
        elif isinstance(report, str):
            lookup = report
        else:
            raise TypeError("report must be of type trustar.models.Report or str")

        response = self._api_client.get(f"reports/{lookup}/status")
        response.raise_for_status()
        result = response.json()

        return result

    # Report Deeplink
    def get_report_deeplink(self, reports_params: ReportsParameters=None):
        """
        Retrieves the TS Station's report deeplink

        :param report: A |Report| or a str object

        :return: A str URL object

        Example:
        >>> report = "fcda196b-eb30-4b59-83b8-a25ab6d70d17"
        >>> deeplink = ts.get_report_deeplink(report)
        >>> isinstance(report, str) or isinstance(report, Report)
        True
        >>> isinstance(deeplink, str)
        True
        >>> print(deeplink)
        """
        report_id = None
        report = reports_params.report

        # default to interal ID if report ID field is present
        # else treat report as an ID string
        try:
            report_id = report.id
        except AttributeError:
            report_id = report

        return f"{self._api_client.station}/constellation/reports/{report_id}"

    # Generators
    def _get_correlated_reports_page_generator(self,
                                               reports_params: ReportsParameters=None,
                                               page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                               page_size=Pagination.DEFAULT_REPORTS_PAGE_SIZE.value
                                               ):
        """
        Creates a generator from the |get_correlated_reports_page| method that
        returns each successive page

        :param indicators: A list of indicator values to retrieve correlated reports for
        :param list(str) enclave_ids: list of enclave ids used to restrict reports
            to specific enclaves (optional - by default reports from all of user's
            enclaves are returned)
        :param is_enclave: Whether to search enclave reports or community reports
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: The generator
        """
        correlated_reports_page_gen = functools.partial(self._get_correlated_reports_page,
                                                        reports_params,)

        return NumberedPage.get_page_generator(correlated_reports_page_gen,
                                               page_number,
                                               page_size)

    def _search_reports_page_generator(self,
                                       reports_params: ReportsParameters=None,
                                       page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                       page_size=Pagination.DEFAULT_REPORTS_PAGE_SIZE.value
                                       ):
        """
        Creates a generator from the |search_reports_page| method that returns
        each successive page

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters
        :param list(str) enclave_ids: list of enclave ids used to restrict reports
            to specific enclaves (optional - by default reports from all of user's
            enclaves are returned)
        :param int from_time: start of time window in milliseconds since epoch (optional)
        :param int to_time: end of time window in milliseconds since epoch (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter reports
            by. Only reports containing ALL of these tags will be returned (optional)
        :param list(str) excluded_tags: Reports containing ANY of these tags will
            be excluded from the results
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: The generator
        """
        search_reports_page_gen = functools.partial(self._search_reports_page,
                                                    reports_params,)

        return NumberedPage.get_page_generator(search_reports_page_gen,
                                               page_number,
                                               page_size)

    # Pages
    def _get_correlated_reports_page(self,
                                     reports_params: ReportsParameters=None,
                                     page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                     page_size=Pagination.DEFAULT_REPORTS_PAGE_SIZE.value
                                     ):
        """
        Retrieves a page of all TruSTAR reports that contain the searched indicators.

        :param indicators: A list of indicator values to retrieve correlated reports for.
        :param enclave_ids: The enclaves to search in.
        :param is_enclave: Whether to search enclave reports or community reports.
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: The list of IDs of correlated reports

        Example:
        >>> reports = ts.get_correlated_reports_page(["wannacry", "www.evil.com"]).items
        >>> print([report.id for report in reports])
        ["e3bc6921-e2c8-42eb-829e-eea8da2d3f36", "4d04804f-ff82-4a0b-8586-c42aef2f6f73"]
        """
        if reports_params.is_enclave:
            distro_type = DistributionType.ENCLAVE
        else:
            distro_type = DistributionType.COMMUNITY

        params = {
            TSReportParameterKeys.INDICATORS.value: reports_params.indicators,
            TSReportParameterKeys.ENCLAVE_IDS.value: reports_params.enclave_ids,
            TSReportParameterKeys.DISTRO_TYPE.value: distro_type,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.get("reports/correlated", params=params)

        return NumberedPage.from_dict(resp.json(), content_type=Report)

    def _search_reports_page(self,
                             reports_params: ReportsParameters=None,
                             page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                             page_size=Pagination.DEFAULT_REPORTS_PAGE_SIZE.value
                             ):
        """
        Search for reports containing a search term.

        :param str search_term: The term to search for.  If empty, no search term
            will be applied.  Otherwise, must be at least 3 characters.
        :param list(str) enclave_ids: list of enclave ids used to restrict reports
            to specific enclaves (optional - by default reports from all of user's
            enclaves are returned)
        :param int from_time: start of time window in milliseconds since epoch (optional)
        :param int to_time: end of time window in milliseconds since epoch (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter reports
            by. Only reports containing ALL of these tags will be returned. (optional)
        :param list(str) excluded_tags: Reports containing ANY of these tags will
            be excluded from the results.
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: a |NumberedPage| of |Report| objects
        `NOTE`:  The bodies of these reports will be `None`
        """
        body = {TSReportParameterKeys.SEARCH_TERM.value: reports_params.search_term}
        params = {
            TSReportParameterKeys.ENCLAVE_IDS.value: reports_params.enclave_ids,
            TSReportParameterKeys.EXCLUDED_TAGS.value: reports_params.excluded_tags,
            TSReportParameterKeys.FROM.value: reports_params.from_time,
            TSReportParameterKeys.TAGS.value: reports_params.tags,
            TSReportParameterKeys.TO.value: reports_params.to_time,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.post("reports/search",
                                     params=params,
                                     data=json.dumps(body))

        return NumberedPage.from_dict(resp.json(), content_type=Report)
