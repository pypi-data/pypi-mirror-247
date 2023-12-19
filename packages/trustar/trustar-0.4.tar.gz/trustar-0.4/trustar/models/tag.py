"""
Defines TS API v1.3 Tag model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import TagKeys


class Tag(ModelBase):
    """
    Models a |Tag| resource

    Schema: https://docs.trustar.co/api/v13/tags/index.html#schema

    :ivar name: The name of the tag, i.e. "malicious"
    :ivar id: The ID of the tag
    :ivar enclave_id: The :class:`Enclave` object representing the enclave that the tag belongs to
    """

    def __init__(self, name, guid=None, enclave_id=None):
        """
        Constructs a tag object

        :param name: The name of the tag, i.e. "malicious"
        :param guid: The ID of the tag
        :param enclave_id: The ID of the enclave the tag belongs to
        """
        self.name = name
        self.guid = guid
        self.enclave_id = enclave_id

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the tag

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the tag
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        return {
            TagKeys.NAME.value: self.name,
            TagKeys.GUID.value: self.guid,
            TagKeys.ENCLAVE_ID.value: self.enclave_id
        }

    @classmethod
    def from_dict(cls, d):
        """
        Creates a tag object from a dictionary `d`

        :param d: The tag dictionary

        :return: A |Tag| object
        """
        return Tag(name=d.get(TagKeys.NAME.value),
                   guid=d.get(TagKeys.GUID.value),
                   enclave_id=d.get(TagKeys.ENCLAVE_ID.value))
