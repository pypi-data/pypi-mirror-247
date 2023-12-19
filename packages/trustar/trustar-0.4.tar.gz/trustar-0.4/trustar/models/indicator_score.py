"""
Defines TS API v1.3 IndicatorScore model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase


class IndicatorScore(ModelBase):
    """
    Models a |IndicatorScore| resource

    Schema: https://docs.trustar.co/api/v13/indicators/get_indicator_summaries.html#indicator-score

    :ivar str name: The name of the score type, e.g. "Risk Score" or
        "Malicious Confidence"
    :ivar str value: The value of the score, as directly extracted from the source
    """

    def __init__(self, name=None, value=None):
        """
        Constructs a |IndicatorScore| object
        """
        self.name = name
        self.value = value

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the indicator score

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the indicator score
        """
        return {'name': self.name, 'value': self.value}

    @classmethod
    def from_dict(cls, d):
        """
        Creates an indicator score object from a dictionary `d`

        :param d: The indicator score dictionary
    
        :return: An |IndicatorScore| object
        """
        return IndicatorScore(name=d.get('name'), value=d.get('value'))
