"""
Defines TS API v1.3 IndicatorAttribute model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import IndicatorAttributeKeys


class IndicatorAttribute(ModelBase):
    """
    Models a |IndicatorAttribute| resource

    Schema: https://docs.trustar.co/api/v13/indicators/get_indicator_summaries.html#indicator-attribute

    :ivar str name: The name of the attribute, e.g. "Actors" or "Malware Families"
    :ivar any value: The value of the attribute, e.g. "North Korea" or "Emotet"
    :ivar str logical_type: Describes how to interpret the `value` field,
        e.g. could be "timestamp" if `value` is an integer
    :ivar str description: A description of how to interpret this attribute. This
        corresponds to the attribute name, i.e. this will be the same for all
        attributes in a source with the same name.
    """

    def __init__(self,
                 name=None,
                 value=None,
                 logical_type=None,
                 description=None):
        """
        Constructs a |IndicatorAttribute| object
        """
        self.name = name
        self.value = value
        self.logical_type = logical_type
        self.description = description

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the indicator attribute.

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the indicator attribute
        """
        return {
            IndicatorAttributeKeys.NAME.value: self.name,
            IndicatorAttributeKeys.VALUE.value: self.value,
            IndicatorAttributeKeys.LOGICAL_TYPE.value: self.logical_type,
            IndicatorAttributeKeys.DESCRIPTION.value: self.description
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates an indicator attribute object from a dictionary `d`

        :param d: The indicator attribute dictionary

        :return: An |IndicatorAttribute| object
        """
        return IndicatorAttribute(name=d.get(IndicatorAttributeKeys.NAME.value),
                                  value=d.get(IndicatorAttributeKeys.VALUE.value),
                                  logical_type=d.get(IndicatorAttributeKeys.LOGICAL_TYPE.value),
                                  description=d.get(IndicatorAttributeKeys.DESCRIPTION.value))
