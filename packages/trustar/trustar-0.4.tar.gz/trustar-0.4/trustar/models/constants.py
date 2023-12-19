"""
Defines TS API v1.3 constant
"""
# ! /usr/local/bin/python3

from enum import Enum


class TruSTARConfig(Enum):
    """
    Supported keys for TruSTAR API 1.3 configuration files
    """
    AUTH = "auth"
    BASE = "base"
    STATION = "station"
    API_KEY = "api_key"
    API_SECRET = "api_secret"
    CLIENT_TYPE = "client_type"
    CLIENT_VERSION = "client_version"
    CLIENT_METATAG = "client_metatag"
    ENCLAVE_IDS = "enclave_ids"
    HTTP = "http"
    HTTP_PROXY = "http_proxy"
    HTTPS = "https"
    HTTPS_PROXY = "https_proxy"
    MAX_WAIT_TIME = "max_wait_time"
    RETRY = "retry"
    VERIFY = "verify"


class TruSTARLegacyConfig(Enum):
    """
    Legacy (DEPRECATED) keys for TruSTAR API 1.3 configuration files
    """
    API_ENDPOINT = "api_endpoint"
    AUTH_ENDPOINT = "auth_endpoint"
    STATION_BASE_URL = "station_base_url"
    USER_API_KEY = "user_api_key"
    USER_API_SECRET = "user_api_secret"


class TSAuth(Enum):
    """
    Available/valid corpus for TS SDK auth operations
    """
    ACCESS_TOKEN = "access_token"
    APP_JSON = "application/json"
    AUTHZ = "Authorization"
    GRANT_TYPE = "grant_type"
    CLIENT_CREDENTIALS = "client_credentials"
    CLIENT_METATAG = "Client-Metatag"
    CLIENT_TYPE = "Client-Type"
    CLIENT_VERSION = "Client-Version"
    CONTENT_TYPE = "Content-Type"


class TSEnclave(Enum):
    """
    Supported keys for EnclavePermissions class
    """
    CREATE = "create"
    READ = "read"
    UPDATE = "update"


class Pagination(Enum):
    """
    Default values for Pagination properties
    """
    DEFAULT_MAX_PAGE_SIZE = 1000
    DEFAULT_PAGE_NUMBER = 0
    DEFAULT_PAGE_SIZE = 100
    DEFAULT_REPORTS_PAGE_SIZE = 25
    DEFAULT_REPORTS_MAX_PAGE_SIZE = 100
    DEFAULT_SUMMARIES_PAGE_SIZE = 25
    DEFAULT_SUMMARIES_MAX_PAGE_SIZE = 100


class TSError(Enum):
    """
    Supported errors corpus for TS SDK operations
    """
    ERROR_DESCRIPTION = "error_description"


class TSFileExtension(Enum):
    """
    Supported corpus of file extensions for TS SDK operations
    """
    CONF = ".conf"
    INI = ".ini"
    JSON = ".json"
    YAML = ".yaml"
    YML = ".yml"


class TSGlossary(Enum):
    """
    Available/valid corpus for TS SDK messages
    """
    CLIENT = "Client"
    SERVER = "Server"
    PYTHON_CONFIG_PATH = "TRUSTAR_PYTHON_CONFIG_PATH"
    PYTHON_CONFIG_ROLE = "TRUSTAR_PYTHON_CONFIG_ROLE"
    TS_CONFIG_FILE = 'trustar.conf'
    TS_CONFIG_ROLE = 'trustar'


class TSIndicatorParameterKeys(Enum):
    """
    Supported pagination corpus for TS SDK Indicators operations
    """
    CONTENT = "content"
    DAYS_BACK = "daysBack"
    ENCLAVE_IDS = "enclaveIds"
    ENTITY_TYPES = "entityTypes"
    EXCLUDED_TAGS = "excludedTags"
    EXCLUDED_TAG_IDS = "excludedTagIds"
    FILENAME = "filename"
    FROM = "from"
    GUID = "guid"
    INDICATOR = "indicator"
    INDICATORS = "indicators"
    INDICATOR_TYPE = "indicatorType"
    INDICATOR_VALUES = "indicatorValues"
    SEARCH_TERM = "searchTerm"
    TAGS = "tags"
    TAG_IDS = "tagIds"
    TYPE = "type"
    TO = "to"
    VALUE = "value"


class TSPaginationKeys(Enum):
    """
    Supported pagination corpus keys for TS SDK operations
    """
    HAS_NEXT = "hasNext"
    ITEMS = "items"
    NEXT_CURSOR = "nextCursor"
    PAGE_NUMBER = "pageNumber"
    PAGE_SIZE = "pageSize"
    RESPONSE_METADATA = "responseMetadata"
    TOTAL_ELEMENTS = "totalElements"


class TSPhishingIndicatorParameterKeys(Enum):
    """
    Supported keys for TS SDK Phishing Indicators operations
    """
    CURSOR = "cursor"
    ENCLAVE_IDS = "enclaveIds"
    FROM = "from"
    NORMALIZED_INDICATOR_SCORE = "normalizedIndicatorScore"
    PRIORITY_EVENT_SCORE = "priorityEventScore"
    STATUS = "status"
    TO = "to"


class TSReportParameterKeys(Enum):
    """
    Supported pagination corpus for TS SDK Reports operations
    """
    DEST_ENCLAVE_ID = "destEnclaveId"
    DISTRO_TYPE = "distributionType"
    ENCLAVE_IDS = "enclaveIds"
    EXCLUDED_TAGS = "excludedTags"
    FROM = "from"
    FROM_SUBMISSION = "copyFromProvidedSubmission"
    ID = "id"
    ID_TYPE = "idType"
    INDICATORS = "indicators"
    MODE = "mode"
    REPORT_BODY = "reportBody"
    REPORT_ID = "reportId"
    SEARCH_TERM = "searchTerm"
    TAGS = "tags"
    TITLE = "title"
    TO = "to"


class TSResponse(Enum):
    """
    Supported response keys for TS SDK operations
    """
    MESSAGE = "message"
    WAIT_TIME = "waitTime"
