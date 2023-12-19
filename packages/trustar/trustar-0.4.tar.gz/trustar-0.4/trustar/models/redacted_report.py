"""
Defines TS API v1.3 RedactedReport model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import ReportKeys


class RedactedReport(ModelBase):
    """
    Models a |RedactedReport| resource

    :ivar title: the report title
    :ivar body: the report body
    """

    def __init__(self, title=None, body=None):
        """
        Constructs a |RedactedReport| object

        :param title: the report title
        :param body: the report body
        """
        self.title = title
        self.body = body

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the object

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the redacted report
        """
        if remove_nones:
            redacted_report_dict = super().to_dict(remove_nones=True)
        else:
            redacted_report_dict = {
                ReportKeys.REPORT_BODY.value: self.body,
                ReportKeys.TITLE.value: self.title
            }

        return redacted_report_dict

    @classmethod
    def from_dict(cls, d):
        """
        Creates a redacted report object from a dictionary `d`

        :param redacted_report: The redacted report dictionary

        :return: A |RedactedReport| object
        """
        return RedactedReport(title=d.get(ReportKeys.TITLE.value),
                              body=d.get(ReportKeys.REPORT_BODY.value))
