"""
Defines TS API v1.3 IndicatorSummary model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import IndicatorSummaryKeys
from .indicator_attribute import IndicatorAttribute
from .indicator_score import IndicatorScore
from .intelligence_source import IntelligenceSource


class IndicatorSummary(ModelBase):
    """
    Models a |IndicatorSummary| resource

    Schema: https://docs.trustar.co/api/v13/indicators/get_indicator_summaries.html#indicator-summary

    :ivar str value: The indicator's value
    :ivar IndicatorType indicator_type: The indicator's type
    :ivar str report_id: The ID of the report for this summary
    :ivar str enclave_id: The ID of the report's enclave
    :ivar IntelligenceSource source: An object containing information about the source
        that the report came from
    :ivar IndicatorScore score: The score of the report, according to the source
    :ivar int created: The created or first seen timestamp of the indicator,
        according to the source
    :ivar int updated: The updated or last seen timestamp of the indicator, according
        to the source
    :ivar str description: The description of the indicator, according to the source
    :ivar list(Attribute) attributes: A list of attributes about the indicator,
        according to the source
    :ivar str severity_level: a normalized representation of the score from this source
        (if one exists). This is an integer between 0 and 3, with 0 being the lowest
        score and 3 being the highest
    """

    def __init__(self,
                 value=None,
                 indicator_type=None,
                 report_id=None,
                 enclave_id=None,
                 source=None,
                 score=None,
                 created=None,
                 updated=None,
                 description=None,
                 attributes=None,
                 severity_level=None):
        """
        Constructs a |IndicatorSummary| object
        """
        self.value = value
        self.indicator_type = indicator_type
        self.report_id = report_id
        self.enclave_id = enclave_id
        self.source = source
        self.score = score
        self.created = created
        self.updated = updated
        self.description = description
        self.attributes = attributes
        self.severity_level = severity_level

    @classmethod
    def from_dict(cls, indicator_summary):
        """
        Create an |IndicatorSummary| object from a dictionary.

        :param indicator_summary: The dictionary.
        :return: The |IndicatorSummary| object.
        """

        attributes = [IndicatorAttribute.from_dict(attribute) for attribute
                      in indicator_summary.get('attributes', [])]

        source = indicator_summary.get('source')
        if source:
            source = IntelligenceSource.from_dict(indicator_summary.get('source'))
            
        score = indicator_summary.get('score')
        if score:
            score = IndicatorScore.from_dict(indicator_summary.get('score'))

        return IndicatorSummary(value=indicator_summary.get('value'),
                                indicator_type=indicator_summary.get('type'),
                                report_id=indicator_summary.get('reportId'),
                                enclave_id=indicator_summary.get('enclaveId'),
                                source=source,
                                score=score,
                                created=indicator_summary.get('created'),
                                updated=indicator_summary.get('updated'),
                                description=indicator_summary.get('description'),
                                attributes=attributes,
                                severity_level=indicator_summary.get('severityLevel'))

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the indicator summary

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the indicator summary
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        source = None
        if self.source:
            source = self.source.to_dict()

        score = None
        if self.score:
            score = self.score.to_dict()

        attributes = None
        if self.attributes:
            attributes = [attribute.to_dict(remove_nones=remove_nones)
                          for attribute in self.attributes]

        return {
            IndicatorSummaryKeys.ATTRIBUTES.value: attributes,
            IndicatorSummaryKeys.CREATED.value: self.created,
            IndicatorSummaryKeys.DESCRIPTION.value: self.description,
            IndicatorSummaryKeys.ENCLAVE_ID.value: self.enclave_id,
            IndicatorSummaryKeys.REPORT_ID.value: self.report_id,
            IndicatorSummaryKeys.SCORE.value: score,
            IndicatorSummaryKeys.SEVERITY_LEVEL.value: self.severity_level,
            IndicatorSummaryKeys.SOURCE.value: source,
            IndicatorSummaryKeys.TYPE.value: self.indicator_type,
            IndicatorSummaryKeys.UPDATED.value: self.updated,
            IndicatorSummaryKeys.VALUE.value: self.value
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates an indicator summary object from a dictionary `d`

        :param indicator_summary: The indicator summary dictionary

        :return: An |IndicatorSummary| object
        """
        attributes = [IndicatorAttribute.from_dict(attribute) for attribute
                      in d.get(IndicatorSummaryKeys.ATTRIBUTES.value, [])]

        source = d.get(IndicatorSummaryKeys.SOURCE.value)
        if source:
            source = IntelligenceSource.from_dict(source)

        score = d.get(IndicatorSummaryKeys.SCORE.value)
        if score:
            score = IndicatorScore.from_dict(score)

        return IndicatorSummary(value=d.get(IndicatorSummaryKeys.VALUE.value),
                                indicator_type=d.get(IndicatorSummaryKeys.TYPE.value),
                                report_id=d.get(IndicatorSummaryKeys.REPORT_ID.value),
                                enclave_id=d.get(IndicatorSummaryKeys.ENCLAVE_ID.value),
                                source=source,
                                score=score,
                                created=d.get(IndicatorSummaryKeys.CREATED.value),
                                updated=d.get(IndicatorSummaryKeys.UPDATED.value),
                                description=d.get(IndicatorSummaryKeys.DESCRIPTION.value),
                                attributes=attributes,
                                severity_level=d.get(IndicatorSummaryKeys.SEVERITY_LEVEL.value))
