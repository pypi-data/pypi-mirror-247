"""
Implements TS API v1.3 Enclaves protocols
"""
# ! /usr/local/bin/python3

# external imports
import functools
import json

# internal imports
from clients.api_client import APIClient
from log import get_logger
from models import EnclavePermissions
from protocols.enclaves_protocol import EnclavesAPI


logger = get_logger(__name__)


class EnclaveClient(EnclavesAPI):
    """
    Class which implements TruSTAR API v1.3 Enclaves protocols

    Enclaves: https://docs.trustar.co/api/v13/enclaves/index.html
    """

    def __init__(self, api_client: APIClient=None):
        """
        Constructs a |EnclaveClient| object
        """
        self._api_client = api_client

    def get_enclaves(self):
        """
        Returns the list of all enclaves that the user has access to, as well
        as whether they can `read`, `create`, and `update` reports in that enclave

        GET `/1.3/enclaves`

        API endpoint docs: https://docs.trustar.co/api/v13/enclaves/get_enclaves.html
        """
        resp = self._api_client.get("enclaves")

        return [EnclavePermissions.from_dict(enclave) for enclave in resp.json()]
