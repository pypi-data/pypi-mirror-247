"""
Implements TruSTAR API v1.3 protocols
"""
# ! /usr/local/bin/python3

# external imports
import configparser
import os
import yaml


# internal imports
from .clients.api_client import APIClient
from .clients.enclave_client import EnclaveClient
from .clients.indicator_client import IndicatorClient
from .clients.phishing_triage_client import PhishingTriageClient
from .clients.report_client import ReportClient
from .clients.tag_client import TagClient

from .log import get_logger
from .models import (
    IndicatorsParameters, ReportsParameters, RequestQuota, TruSTARConfig,
    TruSTARLegacyConfig, TSFileExtension, TSGlossary
)
from .protocols.trustar_protocols import TSAPI as TruStarAPI
from .utils import Utils
from .version import __version__, __api_version__


logger = get_logger(__name__)


# Supported extensions for TS config files
CONF = TSFileExtension.CONF.value
INI = TSFileExtension.INI.value
JSON = TSFileExtension.JSON.value
YAML = TSFileExtension.YAML.value
YML = TSFileExtension.YML.value


class TruStar(TruStarAPI):
    """
    Class which handles TruSTAR API v1.3

    API Documentation: https://docs.trustar.co/api/v13/index.html
    """
    # raise exception if any of these config keys are missing
    REQUIRED_KEYS = (TruSTARConfig.API_KEY.value, TruSTARConfig.API_SECRET.value)

    # log a  warning if any of these config keys are missing
    DESIRED_KEYS = (TruSTARConfig.CLIENT_METATAG.value,)

    # allow configs to use different key names for config values
    REMAPPED_KEYS = {
        TruSTARLegacyConfig.AUTH_ENDPOINT.value: TruSTARConfig.AUTH.value,
        TruSTARLegacyConfig.API_ENDPOINT.value: TruSTARConfig.BASE.value,
        TruSTARLegacyConfig.STATION_BASE_URL.value: TruSTARConfig.STATION.value,
        TruSTARLegacyConfig.USER_API_KEY.value: TruSTARConfig.API_KEY.value,
        TruSTARLegacyConfig.USER_API_SECRET.value: TruSTARConfig.API_SECRET.value
    }

    # default config values
    DEFAULTS = {
        TruSTARConfig.AUTH.value: "https://api.trustar.co/oauth/token",
        TruSTARConfig.BASE.value: "https://api.trustar.co/api/1.3",
        TruSTARConfig.STATION.value: "https://station.trustar.co",
        TruSTARConfig.CLIENT_TYPE.value: 'PYTHON_SDK',
        TruSTARConfig.CLIENT_VERSION.value: __version__,
        TruSTARConfig.CLIENT_METATAG.value: None,
        TruSTARConfig.VERIFY.value: True,
        TruSTARConfig.RETRY.value: True,
        TruSTARConfig.MAX_WAIT_TIME.value: 60,
        TruSTARConfig.HTTP_PROXY.value: None,
        TruSTARConfig.HTTPS_PROXY.value: None
    }

    def __init__(self, config_file=None, config_role=None, config=None):
        """
        Constructs and configures the instance. Initially attempts to use `config`;
        if it is `None`, then attempts to use `config_file` instead.

        The only required config keys are `user_api_key` and `user_api_secret`. 
        To obtain these values, login to TS Station in your browser and
        visit the **API** tab under **SETTINGS** to generate an API key and secret.

        All available config keys, and their defaults, are listed below:

        +--------------------+----------+-----------------------+-------------------------------+
        | key                | required | default               | description                   |
        +====================+==========+=======================+===============================+
        | user_api_key       | Yes      | `True`                | API key                       |
        +--------------------+----------+-----------------------+-------------------------------+
        | user_api_secret    | Yes      | `True`                | API secret                    |
        +--------------------+----------+-----------------------+-------------------------------+
        | enclave_ids        | No       | `[]`                  | A list (or comma-separated    |
        |                    |          |                       | list) of enclave ids          |
        +--------------------+----------+-----------------------+-------------------------------+
        | auth_endpoint      | No       | `"oauth/token"`       | URL to obtain OAuth2 tokens   |
        +--------------------+----------+-----------------------+-------------------------------+
        | api_endpoint       | No       | `"/api/1.3"`          | Base URL for making API calls |
        +--------------------+----------+-----------------------+-------------------------------+
        | station_base_url   | No       | `"station.trustar.co"`| The base URL for Station      |
        +--------------------+----------+-----------------------+-------------------------------+
        | verify             | No       | `True`                | Whether to use SSL            |
        |                    |          |                       | verification                  |
        +--------------------+----------+-----------------------+-------------------------------+
        | retry              | No       | `True`                | Whether to wait and retry     |
        |                    |          |                       | requests that fail with 429   |
        +--------------------+----------+-----------------------+-------------------------------+
        | max_wait_time      | No       | `60`                  | Fail if 429 wait time is      |
        |                    |          |                       | greater than this (seconds)   |
        +--------------------+----------+-----------------------+-------------------------------+
        | client_type        | No       | `"Python_SDK_v1"`     | Client's name being used      |
        +--------------------+----------+-----------------------+-------------------------------+
        | client_version     | No       | Python SDK version    | Client's version being used   |
        +--------------------+----------+-----------------------+-------------------------------+
        | client_metatag     | No(*)    | `None`                | Any additional information    |
        |                    |          |                       | (ex. email address of user)   |
        +--------------------+----------+-----------------------+-------------------------------+
        | http_proxy         | No       | `None`                | http proxy being used         |
        |                    |          |                       | http(s)://user:pwd@{ip}:{port}|
        +--------------------+----------+-----------------------+-------------------------------+
        | https_proxy        | No       | `None`                | https proxy being used        |
        |                    |          |                       | http(s)://user:pwd@{ip}:{port}|
        +--------------------+----------+-----------------------+-------------------------------+

        NOTE (*): It will become mandatory on future versions of trustar,
        please try and update your code accordingly

        :param str config_file: Path to configuration file (conf, json, or yaml). 
            If no value is passed, the environment variable TRUSTAR_PYTHON_CONFIG_FILE
            will be used.  If that is not defined, defaults to `"trustar.conf"`.
        :param str config_role: The section in the configuration file to use.
            If no value is passed, the environment variable TRUSTAR_PYTHON_CONFIG_ROLE
            will be used.  If that is not defined, defaults to `"trustar"`.
        :param dict config: A dictionary of configuration options. This
            will override the config file path passed in the `config_file` parameter.
        """
        self.enclave_ids = "default"
        # attempt to use configuration file if one exists
        if not config:

            # look for config path in environment variable
            if not config_file:
                config_file = os.environ.get(TSGlossary.PYTHON_CONFIG_PATH.value)

            # fallback to config file in current working directory
            if not config_file:
                config_file = TSGlossary.TS_CONFIG_FILE.value

            # look for config role in environment variable
            if not config_role:
                config_role = os.environ.get(TSGlossary.PYTHON_CONFIG_PATH.value)

            # fallback to config role 'trustar'
            if not config_role:
                config_role = TSGlossary.TS_CONFIG_ROLE.value

            config = self.config_from_file(config_file, config_role)
        else:
            # copy so that the dictionary that was passed is not mutated
            config = config.copy()

        config = self._set_ts_defaults(config)

        # initialize api client
        self._api_client = APIClient(config=config)

        self.enclave_client = EnclaveClient(api_client=self._api_client)
        self.indicator_client = IndicatorClient(api_client=self._api_client)
        self.phishing_triage_client = PhishingTriageClient(api_client=self._api_client)
        self.report_client = ReportClient(api_client=self._api_client)
        self.tag_client = TagClient(api_client=self._api_client)

        # get API version and strip "beta" tag
        # This comes from base url passed in config
        # e.g. https://api.trustar.co/api/1.3-beta will give 1.3
        api_version = self._api_client.base.strip("/").split("/")[-1]

        # strip beta tag
        beta_tag = "-beta"
        api_version = api_version.strip(beta_tag)

        # /api resolves to version 1.2
        if api_version.lower() == "api":
            api_version = "1.2"

        # if API version does not match expected version, log a warning
        if api_version.strip(beta_tag) != __api_version__.strip(beta_tag):
            wrong_api_msg = (f"TS Python SDK v({__version__}) is only compatible with TS API "
                             f"v({__api_version__}) but attempted against v({api_version})")
            logger.warning(wrong_api_msg)

        # initialize token property
        self.token = None

    def _set_ts_defaults(self, config: dict=None):
        """
        Fills configuration with defaults values
        """
        # remap config keys names
        for k, v in self.REMAPPED_KEYS.items():
            if k in config and v not in config:
                config[v] = config[k]

        # coerce value to boolean
        verify = config.get(TruSTARConfig.VERIFY.value)
        config[TruSTARConfig.VERIFY.value] = Utils.parse_boolean(verify)

        # coerce value to boolean
        retry = config.get(TruSTARConfig.RETRY.value)
        config[TruSTARConfig.RETRY.value] = Utils.parse_boolean(retry)

        max_wait_time = config.get(TruSTARConfig.MAX_WAIT_TIME.value, None)
        if max_wait_time:
            config[TruSTARConfig.MAX_WAIT_TIME.value] = int(max_wait_time)

        # override Nones with default values if they exist
        for key, val in self.DEFAULTS.items():
            if not config.get(key, None):
                config[key] = val

        # ensure required properties are present
        for key in self.REQUIRED_KEYS:
            if not config.get(key, None):
                raise ValueError(f"Missing config value for {key}")

        # check if desired properties are present
        for key in self.DESIRED_KEYS:
            if config.get(key) is None:
                logger.warning("Key %s will become mandatory", key)

        self.enclave_ids = config.get(TruSTARConfig.ENCLAVE_IDS.value)

        if isinstance(self.enclave_ids, str):
            self.enclave_ids = [self.enclave_ids]

        return config.copy()

    @classmethod
    def config_from_file(cls, config_file_path, config_role):
        """
        Create a configuration dictionary from a config file section. This dictionary
        is what the TruStar class constructor ultimately requires.

        :param config_file_path: The path to the config file.
        :param config_role: The section within the file to use.
        :return: The configuration dictionary.
        """
        # read config file depending on filetype, parse into dictionary
        ext = os.path.splitext(config_file_path)[-1]
        if ext in (CONF, INI):
            config_parser = configparser.RawConfigParser()
            config_parser.read(config_file_path)
            roles = dict(config_parser)
        elif ext in (JSON, YAML, YML):
            with open(config_file_path, "r", encoding="utf-8") as f:
                roles = yaml.safe_load(f)
        else:
            raise IOError(f"Unrecognized filetype for config file '{config_file_path}'")

        # ensure that config file has indicated role
        if config_role in roles:
            config = dict(roles.get(config_role, {}))
        else:
            raise KeyError("Could not find config_role")

        # parse enclave ids
        if TruSTARConfig.ENCLAVE_IDS.value in config:
            # if id has all numeric characters, will be parsed as an int, so convert to string
            enclave_ids = config.get(TruSTARConfig.ENCLAVE_IDS.value)
            if isinstance(enclave_ids, int):
                config[TruSTARConfig.ENCLAVE_IDS.value] = f"{enclave_ids}"
            # split comma separated list if necessary
            if isinstance(enclave_ids, str):
                config[TruSTARConfig.ENCLAVE_IDS.value] = enclave_ids.split(',')
            elif not isinstance(enclave_ids, list):
                enclaves_error_msg = (f"'{TruSTARConfig.ENCLAVE_IDS.value}' must be"
                                      "a list or a comma-separated list")
                raise TypeError(enclaves_error_msg)

            # strip out whitespace
            listed_enclave_ids = [f"{enclave}".strip() for enclave
                                  in config.get(TruSTARConfig.ENCLAVE_IDS.value, None)
                                  if enclave]
            config[TruSTARConfig.ENCLAVE_IDS.value] = listed_enclave_ids
        else:
            # default to empty list
            config[TruSTARConfig.ENCLAVE_IDS.value] = []

        return config

    @classmethod
    def normalize_timestamp(cls, date_time):
        """
        Transforms date_time into an iso8601 int
        """
        return Utils.normalize_timestamp(date_time)

    #####################################################################################
    #########################          TS API Endpoints          ########################
    #####################################################################################

    def get_request_quotas(self):
        """
        Gets the request quotas for the user's company.

        Example:
        >>> ts.get_request_quotas()
        request_quota

        :return: A list of |RequestQuota| objects.
        """
        resp = self._api_client.get("request-quotas")

        return [RequestQuota.from_dict(quota) for quota in resp.json()]

    def get_version(self):
        """
        Gets the version number of the API.

        Example:
        >>> ts.get_version()
        1.3
        """
        result = self._api_client.get("version").content

        if isinstance(result, bytes):
            result = result.decode("utf-8")

        return result.strip("\n")

    def ping(self):
        """
        Pings the API.

        Example:
        >>> ts.ping()
        pong
        """
        result = self._api_client.get("ping").content

        if isinstance(result, bytes):
            result = result.decode("utf-8")

        return result.strip("\n")

    # Enclaves
    @DeprecationWarning("Please invoke get_enclaves instead")
    def get_user_enclaves(self):
        """
        Façade compliant with `EnclavesAPI.get_enclaves` contract

        :return: A list of |EnclavePermissions| objects, each representing an
            enclave and whether the requesting user has `read`, `create`, and
            `update` access to it.
        """
        return self.enclave_client.get_enclaves()

    def get_enclaves(self):
        """
        Façade compliant with `EnclavesAPI.get_enclaves` contract

        :return: A list of |EnclavePermissions| objects, each representing an
            enclave and whether the requesting user has `read`, `create`, and
            `update` access to it.
        """
        return self.enclave_client.get_enclaves()

    # Indicators
    def get_indicators_for_report(self,
                                  indicators_params: IndicatorsParameters=None,
                                  page_number=None,
                                  page_size=None
                                  ):
        """
        Façade compliant with `IndicatorsAPI.get_indicators_for_report` contract
        """
        return self.indicator_client.get_indicators_for_report(indicators_params=indicators_params,
                                                               page_number=page_number,
                                                               page_size=page_size)

    def get_related_indicators(self,
                               indicators_params: IndicatorsParameters=None,
                               page_number=None,
                               page_size=None
                               ):
        """
        Façade compliant with `IndicatorsAPI.get_related_indicators` contract
        """
        return self.indicator_client.get_related_indicators(indicators_params=indicators_params,
                                                            page_number=page_number,
                                                            page_size=page_size)

    def search_indicators(self,
                          indicators_params: IndicatorsParameters=None,
                          page_number=None,
                          page_size=None
                          ):
        """
        Façade compliant with `IndicatorsAPI.search_indicators` contract
        """
        return self.indicator_client.search_indicators(indicators_params=indicators_params,
                                                       page_number=page_number,
                                                       page_size=page_size)

    def get_whitelist(self):
        """
        Façade compliant with `IndicatorsAPI.get_whitelist` contract
        """
        return self.indicator_client.get_whitelist()

    @DeprecationWarning("Please invoke add_to_safelist instead")
    def add_terms_to_whitelist(self, indicators_params: IndicatorsParameters=None):
        """
        Façade (DEPRECATED) compliant with `IndicatorsAPI.add_to_safelist` contract
        """
        return self.add_to_safelist(indicators_params)

    def add_to_safelist(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.add_to_safelist` contract
        """
        return self.indicator_client.add_to_safelist(indicators_params)

    @DeprecationWarning("Please invoke remove_from_safelist instead")
    def delete_indicator_from_whitelist(self,
                                        indicators_params: IndicatorsParameters=None):
        """
        Façade (DEPRECATED) compliant with `IndicatorsAPI.remove_from_safelist` contract
        """
        return self.remove_from_safelist(indicators_params)

    def remove_from_safelist(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.remove_from_safelist` contract
        """
        return self.indicator_client.remove_from_safelist(indicators_params)

    def get_indicator_metadata(self, indicators_params: IndicatorsParameters=None):
        """
        Façade (DEPRECATED) compliant with `IndicatorsAPI.get_indicator_metadata` contract
        """
        return self.indicator_client.get_indicator_metadata(indicators_params)

    def get_indicators_metadata(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.get_indicators_metadata` contract
        """
        return self.indicator_client.get_indicators_metadata(indicators_params)

    def submit_indicators(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.submit_indicators` contract
        """
        return self.indicator_client.submit_indicators(indicators_params)

    def get_indicator_summaries(self,
                                indicators_params: IndicatorsParameters=None,
                                page_number=None,
                                page_size=None
                                ):
        """
        Façade compliant with `IndicatorsAPI.get_indicator_summaries` contract
        """
        return self.indicator_client.get_indicator_summaries(indicators_params=indicators_params,
                                                             page_number=page_number,
                                                             page_size=page_size)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def get_indicators(self,
                       indicators_params: IndicatorsParameters=None,
                       page_number: int=None,
                       page_size: int=None
                       ):
        """
        Façade compliant with `IndicatorsAPI.get_indicators` contract
        """
        return self.indicator_client.get_indicators(indicators_params=indicators_params,
                                                    page_number=page_number,
                                                    page_size=page_size)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def get_indicator_details(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.get_indicator_details` contract
        """
        return self.indicator_client.get_indicator_details(indicators_params)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def get_community_trends(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.get_community_trends` contract
        """
        return self.indicator_client.get_community_trends(indicators_params)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def bulk_indicator_metadata_export(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.bulk_indicator_metadata_export` contract
        """
        return self.indicator_client.bulk_indicator_metadata_export(indicators_params)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def get_indicator_metadata_export_status(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.get_indicator_metadata_export_status` contract
        """
        return self.indicator_client.get_indicator_metadata_export_status(indicators_params)

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    def download_indicator_metadata_export(self, indicators_params: IndicatorsParameters=None):
        """
        Façade compliant with `IndicatorsAPI.download_indicator_metadata_export` contract
        """
        self.indicator_client.download_indicator_metadata_export(indicators_params)

    # Phishing Triage

    # Reports

    # Undocumented and unsupported (FOR INTENAL USAGE ONLY)
    @DeprecationWarning("Please invoke search_reports instead")
    def get_reports(self,
                    reports_params: ReportsParameters=None,
                    page_number: int=None,
                    page_size: int=None
                    ):
        """
        Façade (DEPRECATED) compliant with `ReportsAPI.get_reports` contract
        """
        return self.report_client.search_reports(reports_params=reports_params,
                                                 page_number=page_number,
                                                 page_size=page_size)

    def search_reports(self,
                       reports_params: ReportsParameters=None,
                       page_number: int=None,
                       page_size: int=None
                       ):
        """
        Façade compliant with `ReportsAPI.search_reports` contract
        """
        return self.report_client.search_reports(reports_params=reports_params,
                                                 page_number=page_number,
                                                 page_size=page_size)

    # Tags
