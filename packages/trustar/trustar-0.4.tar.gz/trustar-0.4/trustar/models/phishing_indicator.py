"""
Defines TS API v1.3 PhishingIndicator model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import PhishingIndicatorKeys


class PhishingIndicator(ModelBase):
    """
    Models a |PhishingIndicator| resource

    Schema: https://docs.trustar.co/api/v13/phishing_triage/index.html#phishing-indicators

    :ivar indicator_type: The type of the extracted entity (e.g. URL, IP, ...)
    :ivar value: The value of an extracted entity (e.g. www.badsite.com, etc.)
    :ivar source_key: A string that is associated with the closed source providing context
                       (e.g. 'virustotal', 'crowdstrike_indicator')
    :ivar normalized_indicator_score: The normalized score associated with a context entity
    :ivar original_indicator_score: A score given to the indicator by its original source
    """

    def __init__(self,
                 indicator_type=None,
                 value=None,
                 source_key=None,
                 normalized_indicator_score=None,
                 original_indicator_score=None):
        """
        Constructs a |PhishingIndicator| object
        """
        self.indicator_type = indicator_type
        self.value = value
        self.source_key = source_key
        self.normalized_indicator_score = normalized_indicator_score
        self.original_indicator_score = original_indicator_score

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of a phishing indicator

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the phishing indicator
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        return {
            PhishingIndicatorKeys.INDICATOR_TYPE.value: self.indicator_type,
            PhishingIndicatorKeys.VALUE.value: self.value,
            PhishingIndicatorKeys.SOURCE_KEY.value: self.source_key,
            PhishingIndicatorKeys.NORMALIZED_IOC_SCORE.value: self.normalized_indicator_score,
            PhishingIndicatorKeys.ORIGINAL_IOC_SCORE.value: self.original_indicator_score
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates a phishing indicator object from a dictionary `d`

        :param d: The phishing indicator dictionary

        :return: A |PhishingIndicator| object
        """
        return PhishingIndicator(
            indicator_type=d.get(PhishingIndicatorKeys.INDICATOR_TYPE.value),
            value=d.get(PhishingIndicatorKeys.VALUE.value),
            source_key=d.get(PhishingIndicatorKeys.SOURCE_KEY.value),
            normalized_indicator_score=d.get(PhishingIndicatorKeys.NORMALIZED_IOC_SCORE.value),
            original_indicator_score=d.get(PhishingIndicatorKeys.ORIGINAL_IOC_SCORE.value)
        )
