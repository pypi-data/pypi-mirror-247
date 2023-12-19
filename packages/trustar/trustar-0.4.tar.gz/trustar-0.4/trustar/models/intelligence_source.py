"""
Defines TS API v1.3 IntelligenceSource model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase


class IntelligenceSource(ModelBase):
    """
    Models an |IntelligenceSource| resource

    Schema: https://docs.trustar.co/api/v13/indicators/get_indicator_summaries.html#intelligence-source

    :ivar str key: A string that uniquely identifies the source, e.g. virustotal
    :ivar str name: A human-readable name of the source, as a human-readable
        string, e.g. "VirusTotal"
    """

    def __init__(self, key=None, name=None):
        """
        Constructs an |IntelligenceSource| object
        """
        self.key = key
        self.name = name

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the source

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the source
        """
        return {'key': self.key, 'name': self.name}

    @classmethod
    def from_dict(cls, d):
        """
        Creates an intelligence source object from a dictionary `d`

        :param d: The intelligence source dictionary

        :return: An |IntelligenceSource| object
        """
        return IntelligenceSource(key=d.get('key'), name=d.get('name'))
