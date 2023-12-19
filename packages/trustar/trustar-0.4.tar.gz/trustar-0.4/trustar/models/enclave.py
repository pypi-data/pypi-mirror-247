"""
Defines TS API v1.3 Enclave and EnclavePermissions model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .enum import EnclaveType, EnclavePermissionsKeys


class Enclave(ModelBase):
    """
    Models an |Enclave_resource|.

    :ivar id: The guid of the enclave.
    :ivar name: The name of the enclave.
    """

    def __init__(self, enclave_id, name=None, enclave_type=None):
        """
        Constructs an |Enclave| object.

        :param id: The guid of the enclave.
        :param name: The name of the enclave.
        :param type: The type of enclave.
        """
        self.enclave_id = enclave_id
        self.name = name
        self.enclave_type = enclave_type

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the enclave.

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`
        :return: A dictionary representation of the enclave
        """
        if remove_nones:
            return super().to_dict(remove_nones=True)

        return {
            'id': self.enclave_id,
            'name': self.name,
            'type': self.enclave_type
        }


class EnclavePermissions(Enclave):
    """
    Models an |Enclave_resource| object, but also contains the permissions that the requesting user has to the enclave.
    """

    def __init__(self, id, name=None, type=None, read=None, create=None, update=None):
        """
        Constructs an EnclavePermissions object.

        :param id: The guid of the enclave.
        :param name: The name of the enclave.
        :param type: The type of enclave.
        :param read: Whether the associated user/company has read access.
        :param create: Whether the associated user/company has create access.
        :param update: Whether the associated user/company has update access.
        """

        super().__init__(id, name, type)
        self.read = read
        self.create = create
        self.update = update

    @classmethod
    def from_dict(cls, d):
        """
        Creates an enclave object from a dictionary `d`

        :param d: The enclave dictionary

        :return: An |Enclave| object
        """
        return Enclave(enclave_id=d.get('id'),
                       name=d.get('name'),
                       enclave_type=EnclaveType.from_string(d.get('type')))


class EnclavePermissions(Enclave):
    """
    Models an |EnclavePermissions| resource object, but also contains the
    permissions that the requesting user has to the enclave
    """

    def __init__(self,
                 enclave_id,
                 name=None,
                 enclave_type=None,
                 read=None,
                 create=None,
                 update=None):
        """
        Constructs an |EnclavePermissions| object

        :param enclave_id: The guid of the enclave
        :param name: The name of the enclave
        :param enclave_type: The type of enclave
        :param read: Whether the associated user/company has read access
        :param create: Whether the associated user/company has create access
        :param update: Whether the associated user/company has update access
        """
        super().__init__(enclave_id, name, enclave_type)
        self.read = read
        self.create = create
        self.update = update

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the enclave

        :param remove_nones: Whether `None` values should be filtered out of the
            dictionary. Defaults to `False`

        :return: A dictionary representation of the enclave permissions
        """
        d = super().to_dict(remove_nones=remove_nones)
        d.update({
            EnclavePermissionsKeys.READ.value: self.read,
            EnclavePermissionsKeys.CREATE.value: self.create,
            EnclavePermissionsKeys.UPDATE.value: self.update
        })

        return d

    @classmethod
    def from_dict(cls, d):
        """
        Creates an enclave permission object from a dictionary `d`

        :param d: The enclave permission dictionary

        :return: An |EnclavePermissions| object
        """
        enclave = super(cls, EnclavePermissions).from_dict(d)
        enclave_permissions = cls.from_enclave(enclave)

        enclave_permissions.read = d.get(EnclavePermissionsKeys.READ.value)
        enclave_permissions.create = d.get(EnclavePermissionsKeys.CREATE.value)
        enclave_permissions.update = d.get(EnclavePermissionsKeys.UPDATE.value)

        return enclave_permissions

    @classmethod
    def from_enclave(cls, enclave:Enclave=None):
        """
        Creates an |EnclavePermissions| object from an |Enclave| object

        :param enclave: The Enclave object

        :return: An |EnclavePermissions| object
        """
        return EnclavePermissions(enclave_id=enclave.enclave_id,
                                  name=enclave.name,
                                  enclave_type=enclave.enclave_type)
