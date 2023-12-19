"""
Defines TS API v1.3 PhishingSubmission model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import PhishingSubmissionKeys


class PhishingSubmission(ModelBase):
    """
    Models a |PhishingSubmission| resource

    Schema: https://docs.trustar.co/api/v13/phishing_triage/index.html#phishing-submissions

    `context` is a dictionary containing these fields:
    `indicatorType`, `indicatorValue`, `sourceKey`, `normalizedIndicatorScore`

    :ivar submission_id: The id of the email submission
    :ivar title: The title of the email submission (email subject)
    :ivar priority_event_score: The score of the email submission
    :ivar status: The current triage status of a submission
        ("UNRESOLVED", "CONFIRMED", or "IGNORED")
    :ivar context: A list containing dicts which represent IOCs, sources, and scores
        that contributed to to the triage score.
    """

    def __init__(self,
                 submission_id=None,
                 title=None,
                 priority_event_score=None,
                 status=None,
                 context=None):
        """
        Constructs a |PhishingSubmission| object
        """
        self.submission_id = submission_id
        self.title = title
        self.priority_event_score = priority_event_score
        self.status = status
        self.context = context

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of a phishing submission

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the phishing submission
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        return {
            PhishingSubmissionKeys.CONTEXT.value: self.context,
            PhishingSubmissionKeys.PRIORITY_EVENT_SCORE.value: self.priority_event_score,
            PhishingSubmissionKeys.STATUS.value: self.status,
            PhishingSubmissionKeys.SUBMISSION_ID.value: self.submission_id,
            PhishingSubmissionKeys.TITLE.value: self.title
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates a phishing submission object from a dictionary `d`

        :param d: The phishing submission dictionary

        :return: A |PhishingSubmission| object
        """
        return PhishingSubmission(
            submission_id=d.get(PhishingSubmissionKeys.SUBMISSION_ID.value),
            title=d.get(PhishingSubmissionKeys.TITLE.value),
            priority_event_score=d.get(PhishingSubmissionKeys.PRIORITY_EVENT_SCORE.value),
            status=d.get(PhishingSubmissionKeys.STATUS.value),
            context=d.get(PhishingSubmissionKeys.CONTEXT.value)
        )
