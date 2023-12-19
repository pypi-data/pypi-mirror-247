"""
Defines TS API v1.3 Indicator model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .tag import Tag
from .enum import IndicatorKeys


class Indicator(ModelBase):
    """
    Models an |Indicator| resource

    Schema: https://docs.trustar.co/api/v13/indicators/index.html#schema

    :ivar value: The indicator value; i.e. "www.evil.com"
    :ivar type: The type of indicator; i.e. "URL"
    :ivar priority_level: The priority level of the indicator
    :ivar correlation_count: The number of other indicators that are correlated with
        this indicator.
    :ivar whitelisted: Whether the indicator is whitelisted or not.
    :ivar weight: see |Indicator_resource| for details.
    :ivar reason: see |Indicator_resource| for details.
    :ivar first_seen: the first time this indicator was sighted
    :ivar last_seen: the last time this indicator was sighted
    :ivar sightings: the number of times this indicator has been sighted
    :ivar source: the source that the indicator was observed from
    :ivar notes: a string containing notes about the indicator
    :ivar tags: a list containing |Tag| objects associated with the indicator
    :ivar enclave_ids: a list of enclaves that the indicator is found in
    """

    def __init__(self,
                 value,
                 indicator_type=None,
                 priority_level=None,
                 correlation_count=None,
                 whitelisted=None,
                 weight=None,
                 reason=None,
                 first_seen=None,
                 last_seen=None,
                 sightings=None,
                 source=None,
                 notes=None,
                 tags=None,
                 enclave_ids=None):
        """
        Constructs a |Indicator| object.
        """
        self.value = value
        self.indicator_type = indicator_type
        self.priority_level = priority_level
        self.correlation_count = correlation_count
        self.whitelisted = whitelisted
        self.weight = weight
        self.reason = reason

        # ioc management fields
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.sightings = sightings
        self.source = source
        self.notes = notes
        self.tags = tags
        self.enclave_ids = enclave_ids

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the indicator

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the indicator
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        tags = None
        if self.tags:
            tags = [tag.to_dict(remove_nones=remove_nones) for tag in self.tags]

        return {
            IndicatorKeys.CORRELATION_COUNT.value: self.correlation_count,
            IndicatorKeys.ENCLAVE_IDS.value: self.enclave_ids,
            IndicatorKeys.FIRST_SEEN.value: self.first_seen,
            IndicatorKeys.IOC_TYPE.value: self.indicator_type,
            IndicatorKeys.LAST_SEEN.value: self.last_seen,
            IndicatorKeys.NOTES.value: self.notes,
            IndicatorKeys.PRIORITY_LEVEL.value: self.priority_level,
            IndicatorKeys.REASON.value: self.reason,
            IndicatorKeys.SIGHTINGS.value: self.sightings,
            IndicatorKeys.SOURCE.value: self.source,
            IndicatorKeys.TAGS.value: tags,
            IndicatorKeys.VALUE.value: self.value,
            IndicatorKeys.WEIGHT.value: self.weight,
            IndicatorKeys.WHITELISTED.value: self.whitelisted,
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates an indicator object from a dictionary `d`

        :param d: The indicator dictionary

        :return: An |Indicator| object
        """
        tags = d.get(IndicatorKeys.TAGS.value, [])
        if tags:
            tags = [Tag.from_dict(tag) for tag in tags]

        return Indicator(value=d.get(IndicatorKeys.VALUE.value),
                         indicator_type=d.get(IndicatorKeys.IOC_TYPE.value),
                         priority_level=d.get(IndicatorKeys.PRIORITY_LEVEL.value),
                         correlation_count=d.get(IndicatorKeys.CORRELATION_COUNT.value),
                         whitelisted=d.get(IndicatorKeys.WHITELISTED.value),
                         weight=d.get(IndicatorKeys.WEIGHT.value),
                         reason=d.get(IndicatorKeys.REASON.value),
                         first_seen=d.get(IndicatorKeys.FIRST_SEEN.value),
                         last_seen=d.get(IndicatorKeys.LAST_SEEN.value),
                         sightings=d.get(IndicatorKeys.SIGHTINGS.value),
                         source=d.get(IndicatorKeys.SOURCE.value),
                         notes=d.get(IndicatorKeys.NOTES.value),
                         tags=tags,
                         enclave_ids=d.get(IndicatorKeys.ENCLAVE_IDS.value))
