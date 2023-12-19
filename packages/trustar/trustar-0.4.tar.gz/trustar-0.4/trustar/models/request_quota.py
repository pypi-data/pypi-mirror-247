"""
Defines TS API v1.3 RequestQuota model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import RequestQuotaKeys


class RequestQuota(ModelBase):
    """
    Models a |RequestQuota| resource

    Schema: https://docs.trustar.co/api/v13/request_quotas.html

    :ivar guid: The GUID of the counter.
    :ivar max_requests: The maximum number of requests allowed during the time
        window.
    :ivar used_requests: The number of requests the user has used during the time
        window.
    :ivar time_window: The length of the time window in milliseconds.
    :ivar last_reset_time: The time that the counter was last reset, in milliseconds
        since epoch.
    :ivar next_reset_time: The time that the counter will next be reset, in
        milliseconds since epoch.
    """

    def __init__(self,
                 guid=None,
                 max_requests=None,
                 used_requests=None,
                 time_window=None,
                 last_reset_time=None,
                 next_reset_time=None):
        """
        Constructs an |RequestQuota| object.
        """
        self.guid = guid
        self.max_requests = max_requests
        self.used_requests = used_requests
        self.time_window = time_window
        self.last_reset_time = last_reset_time
        self.next_reset_time = next_reset_time

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of a request quota

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the request quota
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        return {
            RequestQuotaKeys.GUID.value: self.guid,
            RequestQuotaKeys.MAX_REQUESTS.value: self.max_requests,
            RequestQuotaKeys.USED_REQUESTS.value: self.used_requests,
            RequestQuotaKeys.TIME_WINDOW.value: self.time_window,
            RequestQuotaKeys.LAST_RESET_TIME.value: self.last_reset_time,
            RequestQuotaKeys.NEXT_RESET_TIME.value: self.next_reset_time
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates a request quota object from a dictionary `d`

        :param d: The request quota dictionary

        :return: A |RequestQuota| object
        """
        if not d:
            return None

        return RequestQuota(
            guid=d.get(RequestQuotaKeys.GUID.value),
            max_requests=d.get(RequestQuotaKeys.MAX_REQUESTS.value),
            used_requests=d.get(RequestQuotaKeys.USED_REQUESTS.value),
            time_window=d.get(RequestQuotaKeys.TIME_WINDOW.value),
            last_reset_time=d.get(RequestQuotaKeys.LAST_RESET_TIME.value),
            next_reset_time=d.get(RequestQuotaKeys.NEXT_RESET_TIME.value)
        )
