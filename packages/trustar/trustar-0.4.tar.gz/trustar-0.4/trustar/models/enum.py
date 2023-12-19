"""
Defines TS API v1.3 enums for classes
"""
# ! /usr/local/bin/python3

import logging

from enum import Enum


class DistributionType(Enum):
    """
    Distribution types
    """
    COMMUNITY = "COMMUNITY"
    ENCLAVE = "ENCLAVE"


class EnclavePermissionsKeys(Enum):
    """
    Supported keys for EnclavePermissions class
    """
    CREATE = "create"
    READ = "read"
    UPDATE = "update"


class EnclaveType(Enum):
    """
    Enclave types
    """
    CLOSED = "CLOSED"
    CLOSED_CONCRETE = "CLOSED_CONCRETE"
    COMMUNITY = "COMMUNITY"
    INTERNAL = "INTERNAL"
    OPEN = "OPEN"
    OTHER = "OTHER"
    RESEARCH = "RESEARCH"

    @classmethod
    def from_string(cls, string):
        """
        Overrides from_string from Enum for edge cases
        """
        if string == cls.CLOSED_CONCRETE.value:
            return cls.CLOSED

        return super(cls, EnclaveType).from_string(string)


class IdType(Enum):
    """
    Identifier types
    """
    EXTERNAL = "external"
    INTERNAL = "internal"


class IndicatorType(Enum):
    """
    Indicator types
    """
    BITCOIN_ADDRESS = 'BITCOIN_ADDRESS'
    CIDR_BLOCK = 'CIDR_BLOCK'
    CVE = 'CVE'
    EMAIL_ADDRESS = 'EMAIL_ADDRESS'
    IP = 'IP'
    MALWARE = 'MALWARE'
    MD5 = 'MD5'
    REGISTRY_KEY = 'REGISTRY_KEY'
    SHA1 = 'SHA1'
    SHA256 = 'SHA256'
    SOFTWARE = 'SOFTWARE'
    URL = 'URL'

class IndicatorKeys(Enum):
    """
    Supported keys for Indicator attributes
    """
    CORRELATION_COUNT = "correlationCount"
    ENCLAVE_IDS = "enclaveIds"
    FIRST_SEEN = "firstSeen"
    IOC_TYPE = "indicatorType"
    LAST_SEEN = "lastSeen"
    NOTES = "notes"
    PRIORITY_LEVEL = "priorityLevel"
    REASON = "reason"
    SIGHTINGS = "sightings"
    SOURCE = "source"
    TAGS = "tags"
    VALUE = "value"
    WEIGHT = "weight"
    WHITELISTED = "whitelisted"


class IndicatorAttributeKeys(Enum):
    """
    Supported keys for Indicator attributes
    """
    DESCRIPTION = "description"
    LOGICAL_TYPE = "logicalType"
    NAME = "name"
    VALUE = "value"


class IndicatorsKeys(Enum):
    """
    Indicator keys
    """
    CONTENT = "content"
    ENCLAVE_IDS = "enclaveIds"
    TAGS = "tags"


class IndicatorSummaryKeys(Enum):
    """
    Supported keys for IndicatorSummary attributes
    """
    ATTRIBUTES = "attributes"
    CREATED = "created"
    DESCRIPTION = "description"
    ENCLAVE_ID = "enclaveId"
    REPORT_ID = "reportId"
    SCORE = "score"
    SEVERITY_LEVEL = "severityLevel"
    SOURCE = "source"
    TYPE = "type"
    UPDATED = "updated"
    VALUE = "value"


class PhishingIndicatorKeys(Enum):
    """
    Supported keys for PhishingIndicator class
    """
    INDICATOR_TYPE = "indicatorType"
    NORMALIZED_IOC_SCORE = "normalizedIndicatorScore"
    ORIGINAL_IOC_SCORE = "originalIndicatorScore"
    SOURCE_KEY = "sourceKey"
    VALUE = "value"


class PhishingSubmissionKeys(Enum):
    """
    Supported keys for PhishingSubmission class
    """
    CONTEXT = "context"
    PRIORITY_EVENT_SCORE = "priorityEventScore"
    STATUS = "status"
    SUBMISSION_ID = "submissionId"
    TITLE = "title"


class PriorityLevel(Enum):
    """
    Priority levels
    """
    NOT_FOUND = "NOT_FOUND"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ReportKeys(Enum):
    """
    Supported keys for Report attributes
    """
    CREATED = "created"
    DISTRO_TYPE = "distributionType"
    ENCLAVE_IDS = "enclaveIds"
    EXTERNAL_ID = "externalTrackingId"
    EXTERNAL_URL = "externalUrl"
    ID = "id"
    REPORT_BODY = "reportBody"
    TIME_BEGAN = "timeBegan"
    TITLE = "title"
    UPDATED = "updated"


class RequestQuotaKeys(Enum):
    """
    Supported keys for RequestQuota attributes
    """
    GUID = "guid"
    LAST_RESET_TIME = "lastResetTime"
    MAX_REQUESTS = "maxRequests"
    NEXT_RESET_TIME = "nextResetTime"
    TIME_WINDOW = "timeWindow"
    USED_REQUESTS = "usedRequests"


class TagKeys(Enum):
    """
    Supported keys for Tag attributes
    """
    GUID = "guid"
    ENCLAVE_ID = "enclaveId"
    NAME = "name"
