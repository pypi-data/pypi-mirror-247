"""
Implements TS API v1.3 Indicators protocols
"""
# ! /usr/local/bin/python3

# external imports
import functools
import json

# internal imports
from clients.api_client import APIClient
from log import get_logger
from models import (
    Indicator, IndicatorSummary, NumberedPage, Pagination, TSIndicatorParameterKeys,
    TSPaginationKeys
)
from models.parameters.indicators_parameters import IndicatorsParameters
from protocols.indicators_protocol import IndicatorsAPI


logger = get_logger(__name__)


class IndicatorClient(IndicatorsAPI):
    """
    Class implements TruSTAR API v1.3 Indicators protocols

    Indicators: https://docs.trustar.co/api/v13/indicators/index.html
    """

    def __init__(self, api_client: APIClient=None):
        """
        Constructs a |IndicatorClient| object
        """
        self._api_client = api_client

    # API Methods
    def get_indicators_for_report(self,
                                  indicators_params: IndicatorsParameters=None,
                                  page_number: int=None,
                                  page_size: int=None
                                  ):
        """
        Creates a generator that returns each successive indicator for a given report

        :param str report_id: The ID of the report to get indicators for
        :param int page_number: The page number to get
        :param int page_size: The size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        indicators_for_report_page_gen = self._get_indicators_for_report_page_generator(
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=indicators_for_report_page_gen)

    def get_related_indicators(self,
                               indicators_params: IndicatorsParameters=None,
                               page_number: int=None,
                               page_size: int=None
                               ):
        """
        Uses the |get_related_indicators_page| method to create a generator
        that returns each successive report

        :param list(string) indicators: List of indicator values to search for
        :param list(string) enclave_ids: List of GUIDs of enclaves to search in
        :param int page_number: The page number to get
        :param int page_size: The size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        related_indicators_page_gen = self._get_related_indicators_page_generator(
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=related_indicators_page_gen)

    def search_indicators(self,
                          indicators_params: IndicatorsParameters=None,
                          page_number: int=None,
                          page_size: int=None
                          ):
        """
        Uses the |search_indicators_page| method to create a generator that returns
        each successive indicator

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters.
        :param list(str) enclave_ids: List of enclave ids used to restrict indicators
            to specific enclaves (optional - by default indicators from all of user's
            enclaves are returned)
        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(str) indicator_types: A list of indicator types to filter by (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter indicators
            by. Only indicators containing ALL of these tags will be returned. (optional)
        :param list(str) excluded_tags: Indicators containing ANY of these tags will
            be excluded from the results
        :param int page_number: The page number to get
        :param int page_size: The size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        search_indicators_page_gen = self._search_indicators_page_generator(
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=search_indicators_page_gen)

    def get_whitelist(self):
        """
        Uses the |get_whitelist_page| method to create a generator that returns
        each successive whitelisted indicator

        :return: A generator of |Indicator| objects
        """
        safelist_page_gen = self._get_whitelist_page_generator()

        return NumberedPage.get_generator(page_generator=safelist_page_gen)

    def add_to_safelist(self, indicators_params: IndicatorsParameters=None):
        """
        Adds a list of terms to the user's company's whitelist

        :param terms: The list of terms to whitelist

        :return: The list of extracted |Indicator| objects that were whitelisted
        """
        resp = self._api_client.post("whitelist", json=indicators_params.terms)

        return [Indicator.from_dict(indicator) for indicator in resp.json()]

    def remove_from_safelist(self, indicators_params: IndicatorsParameters=None):
        """
        Removes an indicator from the user's company's whitelist

        :param indicator: An |Indicator| object, representing the indicator to delete
        """
        params = indicators_params.indicator.to_dict()

        self._api_client.delete("whitelist", params=params)

    @DeprecationWarning("Please invoke get_indicators_metadata instead")
    def get_indicator_metadata(self, indicators_params: IndicatorsParameters=None):
        """
        Provides metadata associated with a single indicators including `value`,
        `indicatorType`, `noteCount`, `sightings`, `lastSeen`, `enclaveIds`, and `tags`.
        The metadata is determined based on the enclaves the user making the request
        has `READ` access to

        :param indicator_value: An indicator `value` to query

        :return: A dict containing three fields: 'indicator' (an |Indicator| object),
            'tags' (a list of |Tag| objects), and 'enclaveIds' (a list of enclave IDs
            that the indicator was found in)
        """
        result = self.get_indicators_metadata([Indicator(value=indicators_params.indicator_value)])
        if len(result):
            indicator = result[0]
            return {
                TSIndicatorParameterKeys.INDICATOR.value: indicator,
                TSIndicatorParameterKeys.TAGS.value: indicator.tags,
                TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicator.enclave_ids
            }

        return None

    def get_indicators_metadata(self, indicators_params: IndicatorsParameters=None):
        """
        Provides metadata associated with an list of indicators, including value,
        indicatorType, noteCount, sightings, lastSeen, enclaveIds, and tags. The
        metadata is determined based on the enclaves the user making the request
        has `READ` access to

        :param indicators: A list of |Indicator| objects to query. Values are required,
            types are optional. Types might be required to distinguish in a case where
            one indicator value has been associated with multiple types based on
            different contexts.
        :param enclave_ids: A list of enclave IDs to restrict to. By default,
            uses all of the user's enclaves

        :return: A list of |Indicator| objects. The following attributes of the
            objects will be returned: correlation_count, last_seen, sightings,
            notes, tags, enclave_ids. All other attributes of the Indicator objects
            will have Null values
        """
        params = {TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids}
        data = [{
            TSIndicatorParameterKeys.INDICATOR_TYPE.value: i.type,
            TSIndicatorParameterKeys.VALUE.value: i.value
        } for i in indicators_params.indicators]

        resp = self._api_client.post("indicators/metadata",
                                     params=params,
                                     data=json.dumps(data))

        return [Indicator.from_dict(x) for x in resp.json()]

    def submit_indicators(self, indicators_params: IndicatorsParameters=None):
        """
        Submits indicators. The indicator field `value` is required; all other metadata
        fields are optional: `firstSeen`, `lastSeen`, `sightings`, `notes`, and `source`.
        The submission must specify enclaves for the indicators to be submitted to, and
        can optionally specify tags to assign to all the indicators in the submission,
        and/or include individual tags in each Indicator (which will take precedence
        over the submission tags).
        The tags can be existing or new, and are identified by `name` and `enclaveId`.
        (Passing the GUID of an existing tag is not allowed.  `name` and `enclaveId`
        must be specified for each tag.)

        Note that |Indicator| class attribute names are often slightly different
        from the API endpoint's parameters.
        (EX: The |Indicator| class's `first_seen` attribute corresponds to the API
        endpoint's `firstSeen` parameter.)

        :param list(Indicator) indicators: A list of |Indicator| objects. Indicator's 
            `value` is required, all other attributes can be Null.  These |Indicator|
            attributes can be modified / updated using this function: `value`, `first_seen`,
            `last_seen`, `sightings`, `source`, `notes`, and `tags`.
            No other |Indicator| attributes can be modified in TS by using
            this function
        :param list(string) enclave_ids: A list of enclave IDs
        :param list(Tag) tags: A list of |Tag| objects that will be applied to ALL
            indicators in the submission.
            All tags' "id" attribute must be None.
            All tags' "enclave_id" attribute must contain at least one enclave ID.
        """
        tags = []
        enclave_ids = 'default'
        if not indicators_params.enclave_ids:
            no_enclave_ids_msg = (f"IndicatorsAPI missing enclave_ids "
                                  f"({indicators_params.enclave_ids}) for submit_indicators")
            logger.warning(no_enclave_ids_msg)
        else:
            enclave_ids = indicators_params.enclave_ids

        tag_guid_msg = ("'id' attribute on all Tag objects in "
                        "submit_indicators(..) method must be None.")
        tag_enclave_id_msg = ("'enclave_id' attribute for all Tag objects in "
                              "submit_indicators(..) method must contain at "
                              "least one enclave ID.")

        # check entire-submission tag for 'id' & 'enclave_id' compliance.
        if indicators_params.tags:
            for tag in indicators_params.tags:
                if tag.id:
                    raise ValueError(tag_guid_msg)
                if not tag.enclave_id:
                    raise AttributeError(tag_enclave_id_msg)

        # check tags on each indicator for 'id' & 'enclave_id' compliance.
        for indicator in indicators_params.indicators:
            if indicator.tags:
                for tag in indicator.tags:
                    if tag.id:
                        raise ValueError(tag_guid_msg)
                    if not tag.enclave_id:
                        raise AttributeError(tag_enclave_id_msg)

        if indicators_params.tags:
            tags = [tag.to_dict() for tag in indicators_params.tags]

        body = {
            TSIndicatorParameterKeys.CONTENT.value: [indicator.to_dict() for indicator
                                          in indicators_params.indicators],
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: enclave_ids,
            TSIndicatorParameterKeys.TAGS.value: tags
        }

        # NOTE: No generator needed! Direct submission to API
        self._api_client.post("indicators", data=json.dumps(body))

    def get_indicator_summaries(self,
                                indicators_params: IndicatorsParameters=None,
                                page_number=None,
                                page_size=None):
        """
        Creates a generator from the |get_indicator_summaries_page| method that
        returns each successive indicator summary

        :param list(string) values: A list of indicator values to query. These
            must **exactly match** values in TS systems. In order to perform a
            fuzzy match, you must first use the |search_indicators| method to lookup
            the exact indicator values, then provide them to this endpoint.
        :param list(string) enclave_ids: The enclaves to search for indicator summaries
            in. These should be enclaves containing data from sources on the TS Marketplace.
            This parameter is optional, if not provided then all of the user's
            enclaves will be used.
        :param int page_number: The page number to get
        :param int page_size: The size of the page to be returned

        :return: A generator of |IndicatorSummary| objects
        """
        get_indicator_summaries_page_gen = self._get_indicator_summaries_page_generator(
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=get_indicator_summaries_page_gen)

    # Indicators
    def get_indicators(self,
                       indicators_params: IndicatorsParameters=None,
                       page_number=None,
                       page_size=None
                       ):
        """
        Creates a generator from the |get_indicators_page| method that returns each
        successive indicator as an |Indicator| object containing values for the
        'value' and 'type' attributes only; all other |Indicator| object attributes
        will contain Null values

        :param int from_time: Start of time window in milliseconds since epoch
            (defaults to 7 days ago).
        :param int to_time: End of time window in milliseconds since epoch
            (defaults to current time).
        :param list(string) enclave_ids: A list of enclave IDs from which to get
            indicators from. 
        :param list(string) included_tag_ids: Only indicators containing ALL of
            these tag GUIDs will be returned.
        :param list(string) excluded_tag_ids: Only indicators containing
            NONE of these tags GUIDs be returned. 
        :param int page_number: The page number to get
        :param int page_size: The size of the page to be returned
            Passing the integer 1000 as the argument to this parameter should
            result in your script making fewer API calls because it returns the
            largest quantity of indicators with each API call. An API call has to
            be made to fetch each |NumberedPage|

        :return: A generator of |Indicator| objects
        """
        get_indicators_page_gen = self._get_indicators_page_generator(
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size
        )

        return NumberedPage.get_generator(page_generator=get_indicators_page_gen)

    # Indicator Details
    def get_indicator_details(self, indicators, enclave_ids=None):
        """
        Provides a list of indicator values and obtain details for all of them, including
        `indicator_type`, `priority_level`, `correlation_count`, and whether they have
        been whitelisted. Note that the values provided must match indicator values in
        TS Station exactly. If the exact value of an indicator is not known, it
        should be obtained either through the search endpoint first.

        :param indicators: A list of indicator values of any type
        :param enclave_ids: Only find details for indicators in these enclaves

        :return: A list of |Indicator| objects with all fields (except possibly
            `reason`) filled out
        """
        # if the indicators parameter is a string, make it a singleton
        if isinstance(indicators, str):
            indicators = [indicators]

        params = {
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: enclave_ids,
            TSIndicatorParameterKeys.INDICATOR_VALUES.value: indicators
        }
        resp = self._api_client.get("indicators/details", params=params)

        return [Indicator.from_dict(indicator) for indicator in resp.json()]

    # Community Trends
    def get_community_trends(self, indicators_params: IndicatorsParameters=None):
        """
        Find indicators that are trending in the community

        :param indicator_type: A type of indicator to filter by. If `None`, will
            get all types of indicators except for MALWARE and CVEs (this convention
            is for parity with the corresponding view on the Dashboard).
        :param days_back: The number of days back to search. Any integer between
            1 and 30 is allowed

        :return: A list of |Indicator| objects
        """
        params = {
            TSIndicatorParameterKeys.TYPE.value: indicators_params.indicator_type,
            TSIndicatorParameterKeys.DAYS_BACK.value: indicators_params.days_back
        }
        resp = self._api_client.get("indicators/community-trending", params=params)

        # parse items in response as indicators
        return [Indicator.from_dict(indicator) for indicator in resp.json()]

    # Export
    def bulk_indicator_metadata_export(self, indicators_params: IndicatorsParameters=None):
        """
        Initiates a bulk export of indicator metadata

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters.
        :param list(str) enclave_ids: List of enclave ids used to restrict to indicators
            found in reports in specific enclaves (optional - by default reports from
            all of the user's enclaves are used)
        :param int from_time: Start of time window in milliseconds since epoch (optional)
        :param int to_time: End of time window in milliseconds since epoch (optional)
        :param list(str) indicator_types: A list of indicator types to filter by (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter indicators by.
            Only indicators containing ALL of these tags will be returned. (optional)
        :param list(str) excluded_tags: Indicators containing ANY of these tags will
            be excluded from the results

        :return: The guid of the export job
        """
        body = {TSIndicatorParameterKeys.SEARCH_TERM.value: indicators_params.search_term}
        params = {
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids,
            TSIndicatorParameterKeys.ENTITY_TYPES.value: indicators_params.entity_types,
            TSIndicatorParameterKeys.EXCLUDED_TAGS.value: indicators_params.excluded_tags,
            TSIndicatorParameterKeys.FROM.value: indicators_params.from_time,
            TSIndicatorParameterKeys.TAGS.value: indicators_params.tags,
            TSIndicatorParameterKeys.TO.value: indicators_params.to_time
        }

        resp = self._api_client.post("indicators/metadata/bulk-export",
                                     params=params,
                                     data=json.dumps(body))

        return resp.json().get('guid')

    def get_indicator_metadata_export_status(self, indicators_params: IndicatorsParameters=None):
        """
        Get the status of a currently running indicator metadata export job.
        The result will be one of RUNNING, ERROR, or COMPLETE

        :param str guid: The guid of the export job

        :return: The status of the export job
        """
        bulk_exp_status_url =  f"indicators/metadata/bulk-export/{indicators_params.guid}/status"
        resp = self._api_client.get(bulk_exp_status_url)

        return resp.json().get('status')

    def download_indicator_metadata_export(self, indicators_params: IndicatorsParameters=None):
        """
        Download the contents of a COMPLETE export job to the file specified
        by filename

        :param str guid: The guid of the export job
        :param str filename: The name of the file to save the contents
        """
        guid_filepath = f"indicators/metadata/bulk-export/{indicators_params.guid}/data.csv"
        with self._api_client.get(guid_filepath, stream=True) as stream_response:
            stream_response.raise_for_status()
            # NOTE: Question for Ecosystems team: Should we update to 'wb+' for being safer?
            with open(indicators_params.filename, 'wb', encoding="utf-8") as f:
                for chunk in stream_response.iter_content(chunk_size=8192):
                    f.write(chunk)

    # Generators
    def _get_indicators_for_report_page_generator(self,
                                                  indicators_params: IndicatorsParameters=None,
                                                  page_number=None,
                                                  page_size=None
                                                  ):
        """
        Creates a generator from the |get_indicators_for_report_page| method that
        returns each successive page

        :param str report_id: The ID of the report to get indicators for
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        get_report_indicators_page_gen = functools.partial(self._get_indicators_for_report_page,
                                                           indicators_params=indicators_params)

        return NumberedPage.get_page_generator(get_report_indicators_page_gen,
                                               page_number,
                                               page_size)

    def _get_related_indicators_page_generator(self,
                                               indicators_params: IndicatorsParameters=None,
                                               page_number=None,
                                               page_size=None
                                               ):
        """
        Creates a generator from the |get_related_indicators_page| method that returns each
        successive page

        :param indicators: list of indicator values to search for
        :param enclave_ids: list of IDs of enclaves to search in
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        get_related_indicators_page_gen = functools.partial(self._get_related_indicators_page,
                                                            indicators_params)

        return NumberedPage.get_page_generator(get_related_indicators_page_gen,
                                               page_number,
                                               page_size)

    def _search_indicators_page_generator(self,
                                          indicators_params: IndicatorsParameters=None,
                                          page_number=None,
                                          page_size=None
                                          ):
        """
        Creates a generator from the |search_indicators_page| method that returns
        each successive page

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters
        :param list(str) enclave_ids: list of enclave ids used to restrict indicators
            to specific enclaves (optional - by default indicators from all of user's
            enclaves are returned)
        :param int from_time: start of time window in milliseconds since epoch (optional)
        :param int to_time: end of time window in milliseconds since epoch (optional)
        :param list(str) indicator_types: a list of indicator types to filter by (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter indicators by.
            Only indicators containing ALL of these tags will be returned. (optional)
        :param list(str) excluded_tags: Indicators containing ANY of these tags will
            be excluded from the results
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        search_indicators_page_gen = functools.partial(self._search_indicators_page,
                                                       indicators_params=indicators_params)

        return NumberedPage.get_page_generator(search_indicators_page_gen, page_number, page_size)

    def _get_whitelist_page_generator(self, page_number=None, page_size=None):
        """
        Creates a generator from the |get_whitelist_page| method that returns each
        successive page

        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        return NumberedPage.get_page_generator(self._get_whitelist_page, page_number, page_size)

    def _get_indicator_summaries_page_generator(self,
                                                indicators_params: IndicatorsParameters=None,
                                                page_number=None,
                                                page_size=None
                                                ):
        """
        Creates a generator from the |get_indicator_summaries_page| method that
        returns each successive page

        :param list(string) values: A list of indicator values to query. These must
            **exactly match** values in TS systems. In order to perform a fuzzy match,
            you must first use the |search_indicators| method to lookup the exact
            indicator values, then provide them to this endpoint
        :param list(string) enclave_ids: The enclaves to search for indicator summaries
            in. These should be enclaves containing data from sources on TS Marketplace.
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |IndicatorSummary| objects
        """
        get_indicator_summaries_page_gen = functools.partial(self._get_indicator_summaries_page,
                                                         indicators_params=indicators_params)

        return NumberedPage.get_page_generator(get_indicator_summaries_page_gen,
                                               page_number,
                                               page_size)

    def _get_indicators_page_generator(self,
                                       indicators_params: IndicatorsParameters=None,
                                       page_number=None,
                                       page_size=None
                                       ):
        """
        Creates a generator from the |get_indicators_page| method that returns
        each successive page

        :param int from_time: start of time window in milliseconds since epoch
            (defaults to 7 days ago)
        :param int to_time: end of time window in milliseconds since epoch (defaults
            to current time)
        :param list(string) enclave_ids: a list of enclave IDs to filter by
        :param list(string) included_tag_ids: only indicators containing ALL of
            these tags will be returned
        :param list(string) excluded_tag_ids: only indicators containing NONE of
            these tags will be returned
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A generator of |Indicator| objects
        """
        get_indicators_page_gen = functools.partial(
            self._get_indicators_page,
            indicators_params=indicators_params,
            page_number=page_number,
            page_size=page_size,
        )

        return NumberedPage.get_page_generator(get_indicators_page_gen, page_number, page_size)

    # Pages
    def _get_indicators_for_report_page(self,
                                       indicators_params: IndicatorsParameters=None,
                                       page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                       page_size=Pagination.DEFAULT_PAGE_SIZE.value
                                       ):
        """
        Gets a page of the indicators that were extracted from a report

        :param str report_id: the ID of the report to get the indicators for
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of Indicator objects
        """
        params = {
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }
        resp = self._api_client.get(f"reports/{indicators_params.report_id}/indicators",
                                    params=params)

        return NumberedPage.from_dict(resp.json(), content_type=Indicator)

    def _get_related_indicators_page(self,
                                    indicators_params: IndicatorsParameters=None,
                                    page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                    page_size=Pagination.DEFAULT_PAGE_SIZE.value):
        """
        Finds all reports that contain any of the given indicators and returns
        correlated indicators from those reports

        :param indicators: list of indicator values to search for
        :param enclave_ids: list of IDs of enclaves to search in
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of Indicator objects
        """
        params = {
            TSIndicatorParameterKeys.INDICATORS.value: indicators_params.indicators,
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.get("indicators/related", params=params)

        return NumberedPage.from_dict(resp.json(), content_type=Indicator)

    def _search_indicators_page(self,
                               indicators_params: IndicatorsParameters=None,
                               page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                               page_size=Pagination.DEFAULT_PAGE_SIZE.value
                               ):
        """
        Searches for indicators containing a search term

        :param str search_term: The term to search for. If empty, no search term
            will be applied. Otherwise, must be at least 3 characters
        :param list(str) enclave_ids: list of enclave ids used to restrict to
            indicators found in reports in specific enclaves (optional - by default
            reports from all of the user's enclaves are used)
        :param int from_time: start of time window in milliseconds since epoch (optional)
        :param int to_time: end of time window in milliseconds since epoch (optional)
        :param list(str) indicator_types: a list of indicator types to filter by (optional)
        :param list(str) tags: Name (or list of names) of tag(s) to filter indicators by.
            Only indicators containing ALL of these tags will be returned. (optional)
        :param list(str) excluded_tags: Indicators containing ANY of these tags
            will be excluded from the results
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of Indicator objects
        """
        body = {TSIndicatorParameterKeys.SEARCH_TERM.value: indicators_params.search_term}
        params = {
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids,
            TSIndicatorParameterKeys.ENTITY_TYPES.value: indicators_params.entity_types,
            TSIndicatorParameterKeys.EXCLUDED_TAGS.value: indicators_params.excluded_tags,
            TSIndicatorParameterKeys.FROM.value: indicators_params.from_time,
            TSIndicatorParameterKeys.TAGS.value: indicators_params.tags,
            TSIndicatorParameterKeys.TO.value: indicators_params.to_time,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.post("indicators/search",
                                     params=params,
                                     data=json.dumps(body))

        return NumberedPage.from_dict(resp.json(), content_type=Indicator)

    def _get_whitelist_page(self, page_number=0, page_size=100):
        """
        Gets a paginated list of indicators that the user's company has whitelisted

        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of Indicator objects
        """
        params = {
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.get("whitelist", params=params)

        return NumberedPage.from_dict(resp.json(), content_type=Indicator)

    def _get_indicator_summaries_page(self,
                                     indicators_params: IndicatorsParameters=None,
                                     page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                                     page_size=Pagination.DEFAULT_SUMMARIES_PAGE_SIZE.value
                                     ):
        """
        Provides structured summaries about indicators, which are derived from
        intelligence sources on the TruSTAR Marketplace

        :param list(string) values: A list of indicator values to query. These must
            **exactly match** values in TS systems. In order to perform a fuzzy match,
            you must first use the |search_indicators| method to lookup the exact
            indicator values, then provide them to this endpoint
        :param list(string) enclave_ids: The enclaves to search for indicator summaries
            in. These should be enclaves containing data from sources on TS Marketplace
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of IndicatorSummary objects
        """
        params = {
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.post("indicators/summaries",
                                     json=indicators_params.values,
                                     params=params)

        return NumberedPage.from_dict(resp.json(), IndicatorSummary)

    def _get_indicators_page(self,
                            indicators_params: IndicatorsParameters=None,
                            page_number=Pagination.DEFAULT_PAGE_NUMBER.value,
                            page_size=Pagination.DEFAULT_PAGE_SIZE.value
                            ):
        """
        Gets a page of indicators matching the provided filters

        :param int from_time: start of time window in milliseconds since epoch.
            Defaults to 7 days ago
        :param int to_time: end of time window in milliseconds since epoch.
            Defaults to current time
        :param list(string) enclave_ids: a list of enclave IDs to filter by
        :param list(string) included_tag_ids: only indicators containing ALL of
            these tags will be returned
        :param list(string) excluded_tag_ids: only indicators containing NONE of
            these tags will be returned
        :param int page_number: the page number to get
        :param int page_size: the size of the page to be returned

        :return: A |NumberedPage| of Indicator objects
        """
        params = {
            TSIndicatorParameterKeys.ENCLAVE_IDS.value: indicators_params.enclave_ids,
            TSIndicatorParameterKeys.EXCLUDED_TAG_IDS.value: indicators_params.excluded_tag_ids,
            TSIndicatorParameterKeys.FROM.value: indicators_params.from_time,
            TSIndicatorParameterKeys.TAG_IDS.value: indicators_params.included_tag_ids,
            TSIndicatorParameterKeys.TO.value: indicators_params.to_time,
            TSPaginationKeys.PAGE_NUMBER.value: page_number,
            TSPaginationKeys.PAGE_SIZE.value: page_size
        }

        resp = self._api_client.get("indicators", params=params)

        return NumberedPage.from_dict(resp.json(), content_type=Indicator)
