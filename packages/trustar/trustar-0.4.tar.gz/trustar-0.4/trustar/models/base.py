"""
Defines TS API v1.3 Base model
"""
# ! /usr/local/bin/python3

from utils import Utils


class ModelBase:
    """
    This is the base class for all models
    """

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the object

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: The dictionary representation
        """
        if remove_nones:
            return Utils.remove_nones(self.to_dict())

        raise NotImplementedError()

    @classmethod
    def from_dict(cls, d):
        """
        Creates an instance of the class from a dictionary `d` representation

        :return: The instance
        """
        raise NotImplementedError()

    def __str__(self):
        """
        :return: A string representation of the object
        """
        return f"{self.to_dict(remove_nones=True)}"

    def __repr__(self):
        """
        :return: The string representation of the object
        """
        return f"{self}"
