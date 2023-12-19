"""
Implements TS API v1.3 Phishing Triage protocols
"""
# ! /usr/local/bin/python3

# external imports
import json
import functools

# internal imports
from clients.api_client import APIClient
from models import (
    CursorPage, PhishingIndicator, PhishingSubmission, TSPaginationKeys,
    TSPhishingIndicatorParameterKeys
)
from protocols.phising_triage_protocol import PhishingTriageAPI, PhishingTriageParameters
from utils import Utils


class PhishingTriageClient(PhishingTriageAPI):
    """
    Class which implements TruSTAR API v1.3 Phishing Triage protocols
    """

    def __init__(self, api_client: APIClient=None):
        """
        Constructs a |PhishingTriageClient| object
        """
        self._api_client = api_client

    # API Methods
    def get_phishing_submissions(self, phishing_triage_params: PhishingTriageParameters=None):
        """
        Fetches all phishing submissions that fit a given criteria

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) priority_event_score: List of desired scores of phishing submission
            on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: List of enclave ids to pull submissions from.
                                         (defaults to all of a user's enclaves)
        :param list(string) status: List of statuses to filter submissions by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param string cursor: A Base64-encoded string that contains information on how
            to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0

        :return: CursorPage.generator - A generator object which can be used to
            paginate through |PhishingSubmission| data
        """
        phishing_submissions_page_gen = self._get_phishing_submissions_page_generator(
            phishing_triage_params=phishing_triage_params,
        )

        return CursorPage.get_generator(page_generator=phishing_submissions_page_gen)

    def set_triage_status(self, phishing_triage_params: PhishingTriageParameters=None):
        """
        Marks a phishing email submission with one of the phishing namespace tags

        :param string submission_id: ID of the email submission
        :param string status: Triage status of submission
        """
        phishing_triage_sub_id = phishing_triage_params.submission_id
        if not phishing_triage_sub_id or not isinstance(phishing_triage_sub_id, str):
            raise AttributeError("Provide submission ID of phishing email to set triage status")

        params = {TSPhishingIndicatorParameterKeys.STATUS.value: phishing_triage_params.status}

        return self._api_client.post(f"triage/submissions/{phishing_triage_sub_id}/status",
                                     params=params)

    def get_phishing_indicators(self, phishing_triage_params: PhishingTriageParameters=None):
        """
        Get a page of phishing indicators that match the given criteria

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) normalized_indicator_score: List of desired scores of intel sources
            on a scale of 0-3 (default: [3])
        :param list(int) priority_event_score: List of desired scores of phishing
            indicators on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: A list of enclave IDs to filter by.
            (defaults to all of a user's enclaves)
        :param list(string) status: List of statuses to filter indicators by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param string cursor: A Base64-encoded string that contains information on
            how to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0

        :return: CursorPage.generator - A generator object which can be used to
            paginate through |PhishingIndicator| data
        """
        phishing_indicators_page_gen = self._get_phishing_indicators_page_generator(
            phishing_triage_params=phishing_triage_params,
        )

        return CursorPage.get_generator(page_generator=phishing_indicators_page_gen)

    # Generators
    def _get_phishing_submissions_page_generator(self,
                                                 phishing_triage_params: PhishingTriageParameters=None):
        """
        Creates a generator from the |_get_phishing_submissions_page| method that
        returns each successive page

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) priority_event_score: List of desired scores of phishing
            submission on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: A list of enclave IDs to filter by.
            (defaults to all of a user's enclaves)
        :param list(string) status: List of statuses to filter submissions by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param string cursor: A Base64-encoded string that contains information on how
            to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0
        """
        phishing_submissions_page = functools.partial(
            self._get_phishing_submissions_page,
            phishing_triage_params=phishing_triage_params,
        )

        return CursorPage.get_cursor_based_page_generator(phishing_submissions_page,
                                                          cursor=phishing_triage_params.cursor)

    def _get_phishing_indicators_page_generator(self,
                                                phishing_triage_params: PhishingTriageParameters=None):
        """
        Creates a generator from the |_get_phishing_indicators_page| method that
        returns each successive page

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) normalized_indicator_score: List of desired scores of intel sources
            on a scale of 0-3 (default: [3])
        :param list(int) priority_event_score: List of desired scores of phishing
            indicators on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: A list of enclave IDs to filter by
            (defaults to all of a user's enclaves)
        :param list(string) status: List of statuses to filter indicators by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param string cursor: A Base64-encoded string that contains information on
            how to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0
        """
        phishing_indicators_page = functools.partial(
            self._get_phishing_indicators_page,
            phishing_triage_params=phishing_triage_params,
        )

        return CursorPage.get_cursor_based_page_generator(phishing_indicators_page,
                                                          cursor=phishing_triage_params.cursor)

    # Pages
    def _get_phishing_submissions_page(self,
                                      phishing_triage_params: PhishingTriageParameters=None,
                                      page_size=None):
        """
        Get a page of phishing submissions that match the given criteria

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) priority_event_score: List of desired scores of phishing
            submission on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: A list of enclave IDs to filter by
            (defaults to all of a user's enclaves)
        :param list(string) status: List of statuses to filter submissions by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param int page_size: Size of the page to be returned. Max value possible is
            1000. Default is 25
        :param string cursor: A Base64-encoded string that contains information on how
            to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0

        :return: |CursorPage| - An object representing a single page of
            |PhishingSubmission| objects
        """
        params = {TSPaginationKeys.PAGE_SIZE.value: page_size}
        data = Utils.remove_nones({
            TSPhishingIndicatorParameterKeys.CURSOR.value: phishing_triage_params.cursor,
            TSPhishingIndicatorParameterKeys.ENCLAVE_IDS.value: phishing_triage_params.enclave_ids,
            TSPhishingIndicatorParameterKeys.FROM.value: phishing_triage_params.from_time,
            TSPhishingIndicatorParameterKeys.PRIORITY_EVENT_SCORE.value: phishing_triage_params.priority_event_score,
            TSPhishingIndicatorParameterKeys.STATUS.value: phishing_triage_params.status,
            TSPhishingIndicatorParameterKeys.TO.value: phishing_triage_params.to_time
        })

        resp = self._api_client.post("triage/submissions",
                                     params=params,
                                     data=json.dumps(data))

        return CursorPage.from_dict(resp.json(), content_type=PhishingSubmission)

    def _get_phishing_indicators_page(self,
                                     phishing_triage_params: PhishingTriageParameters=None,
                                     page_size=None):
        """
        Get a page of phishing indicators that match the given criteria

        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(int) normalized_indicator_score: List of desired scores of intel sources
            on a scale of 0-3 (default: [3])
        :param list(int) priority_event_score: List of desired scores of phishing
            indicators on a scale of 0-3 (default: [3])
        :param list(string) enclave_ids: A list of enclave IDs to filter by
        :param list(string) status: List of statuses to filter indicators by.
            Options are 'UNRESOLVED', 'CONFIRMED', and 'IGNORED'. (default: ['UNRESOLVED'])
        :param int page_size: Size of the page to be returned. Max value possible
            is 1000. Default is 25
        :param string cursor: A Base64-encoded string that contains information on
            how to retrieve the next page. If a cursor isn't passed, it will default to
            pageSize: 25, pageNumber: 0

        :return: |CursorPage| - An object representing a single page of 
            |PhishingIndicator| objects
        """
        params = {TSPaginationKeys.PAGE_SIZE.value: page_size}
        data = Utils.remove_nones({
            TSPhishingIndicatorParameterKeys.CURSOR.value: phishing_triage_params.cursor,
            TSPhishingIndicatorParameterKeys.ENCLAVE_IDS.value: phishing_triage_params.enclave_ids,
            TSPhishingIndicatorParameterKeys.FROM.value: phishing_triage_params.from_time,
            TSPhishingIndicatorParameterKeys.NORMALIZED_INDICATOR_SCORE.value: phishing_triage_params.normalized_indicator_score,
            TSPhishingIndicatorParameterKeys.PRIORITY_EVENT_SCORE.value: phishing_triage_params.priority_event_score,
            TSPhishingIndicatorParameterKeys.STATUS.value: phishing_triage_params.status,
            TSPhishingIndicatorParameterKeys.TO.value: phishing_triage_params.to_time
        })

        resp = self._api_client.post("triage/indicators",
                                     params=params,
                                     data=json.dumps(data))

        return CursorPage.from_dict(resp.json(), content_type=PhishingIndicator)
