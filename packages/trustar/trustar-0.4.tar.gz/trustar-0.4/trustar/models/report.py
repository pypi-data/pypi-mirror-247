"""
Defines TS API v1.3 Report model
"""
# ! /usr/local/bin/python3

# internal imports
from utils import Utils
from .base import ModelBase
from .enum import DistributionType, IdType, ReportKeys


class Report(ModelBase):
    """
    Models a |Report| resource

    Schema: https://docs.trustar.co/api/v13/reports/index.html#schema

    :ivar id: the report guid
    :ivar title: the report title
    :ivar body: the report body
    :ivar time_began: the time that the incident began; either an integer
        (milliseconds since epoch) or an isoformat datetime string
    :ivar external_id: An external tracking id. For instance, if the report is a
        copy of a corresponding report in some external system, this should contain
        its id in that system.
    :ivar external_url: A URL to the report in an external system (if one exists)
    :ivar is_enclave: A boolean representing whether the distribution type of the
        report is ENCLAVE or COMMUNITY.
    :ivar enclave_ids: A list of IDs of enclaves that the report belongs to
    """
    ID_TYPE_INTERNAL = IdType.INTERNAL
    ID_TYPE_EXTERNAL = IdType.EXTERNAL

    DISTRO_TYPE_ENCLAVE = DistributionType.ENCLAVE
    DISTRO_TYPE_COMMUNITY = DistributionType.COMMUNITY

    def __init__(self,
                 id=None,
                 title=None,
                 body=None,
                 time_began=None,
                 external_id=None,
                 external_url=None,
                 is_enclave=True,
                 enclave_ids=None,
                 created=None,
                 updated=None):
        """
        Constructs a |Report| object

        :param id: the report guid
        :param title: the report title
        :param body: the report body
        :param time_began: the time that the incident began; either an integer
            (milliseconds since epoch) or an isoformat datetime string
        :param external_id: An external tracking id. For instance, if the report
            is a copy of a corresponding report in some external system, this should
            contain its id in that system
        :param external_url: A URL to the report in an external system (if one exists)
        :param is_enclave: A boolean representing whether the distribution type
            of the report is ENCLAVE or COMMUNITY
        :param enclave_ids: The list of enclave_ids the report is associated with.
            If `is_enclave` is `True`, this cannot be `None` or empty
        """
        # default to distribution type ENCLAVE
        if is_enclave is None:
            is_enclave = True

        self.id = id
        self.title = title
        self.body = body
        self.external_id = external_id
        self.external_url = external_url
        self.is_enclave = is_enclave
        self.enclave_ids = enclave_ids
        self.created = created
        self.updated = updated

        self.set_time_began(time_began)

        if isinstance(self.enclave_ids, str):
            self.enclave_ids = [self.enclave_ids]

    def set_time_began(self, time_began):
        """
        :return: An ISO 8601 int or str with a normalized timestamp
        """
        self.time_began = Utils.normalize_timestamp(time_began)

    def _get_distribution_type(self):
        """
        :return: A string indicating whether the report belongs to an enclave or not.
        """
        return self.DISTRO_TYPE_ENCLAVE if self.is_enclave else self.DISTRO_TYPE_COMMUNITY

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the object

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the report
        """
        if remove_nones:
            report_dict = super().to_dict(remove_nones=True)
        else:
            report_dict = {
                ReportKeys.CREATED.value: self.created,
                ReportKeys.DISTRO_TYPE.value: self._get_distribution_type(),
                ReportKeys.ENCLAVE_IDS.value: self.enclave_ids,
                ReportKeys.EXTERNAL_ID.value: self.external_id,
                ReportKeys.EXTERNAL_URL.value: self.external_url,
                ReportKeys.REPORT_BODY.value: self.body,
                ReportKeys.TIME_BEGAN.value: self.time_began,
                ReportKeys.TITLE.value: self.title,
                ReportKeys.UPDATED.value: self.updated
            }

        # id field might not be present
        report_dict[ReportKeys.ID.value] = self.id if self.id else None

        return report_dict

    @classmethod
    def from_dict(cls, d):
        """
        Creates a report object from a dictionary `d`

        :param d: The report dictionary

        :return: A |Report| object
        """
        # determine distribution type
        distribution_type = d.get(ReportKeys.DISTRO_TYPE.value)
        if distribution_type is not None:
            is_enclave = distribution_type.upper() != DistributionType.COMMUNITY
        else:
            is_enclave = None

        return Report(id=d.get(ReportKeys.ID.value),
                      title=d.get(ReportKeys.TITLE.value),
                      body=d.get(ReportKeys.REPORT_BODY.value),
                      time_began=d.get(ReportKeys.TIME_BEGAN.value),
                      external_id=d.get(ReportKeys.EXTERNAL_ID.value),
                      external_url=d.get(ReportKeys.EXTERNAL_URL.value),
                      is_enclave=is_enclave,
                      enclave_ids=d.get(ReportKeys.ENCLAVE_IDS.value),
                      created=d.get(ReportKeys.CREATED.value),
                      updated=d.get(ReportKeys.UPDATED.value))
