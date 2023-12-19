"""
TS API v1.3 client
"""
# ! /usr/local/bin/python3

# external imports
import json
import requests
import requests.auth
import time
from math import ceil
from requests import HTTPError

# internal imports
from log import get_logger
from models.constants import (
    TruSTARConfig, TSAuth, TSError, TSGlossary, TSResponse
)


logger = get_logger(__name__)


CLIENT = TSGlossary.CLIENT.value
SERVER = TSGlossary.SERVER.value


class APIClient:
    """
    This class is used to make HTTP requests to the TruSTAR API.
    """

    def __init__(self, config: dict=None):
        """
        Constructs and configures the instance. Initially attempts to use `config`;
        if it is `None`, then attempts to use `config_file` instead.

        The only required config keys are `user_api_key` and `user_api_secret`.
        To obtain these values, login to TS Station in your browser and visit the
        **API** tab under **SETTINGS** to generate an API key and secret.

        All available keys, and their defaults, are listed below:

        +-------------------------+--------------------------------------------------------+
        | key                     | description                                            |
        +=========================+========================================================+
        | user_api_key            | API key                                                |
        +-------------------------+--------------------------------------------------------+
        | user_api_secret         | API secret                                             |
        +-------------------------+--------------------------------------------------------+
        | auth_endpoint           | The URL used to obtain OAuth2 tokens                   |
        +-------------------------+--------------------------------------------------------+
        | api_endpoint            | The base URL used for making API calls                 |
        +-------------------------+--------------------------------------------------------+
        | station_base_url        | The base URL for Station                               |
        +-------------------------+--------------------------------------------------------+
        | verify                  | Whether to use SSL verification                        |
        +-------------------------+--------------------------------------------------------+
        | retry                   | Whether to wait and retry requests that fail with 429  |
        +-------------------------+--------------------------------------------------------+
        | max_wait_time           | Allow to fail if 429 wait time is greater than this    |
        +-------------------------+--------------------------------------------------------+
        | client_type             | The name of the client being used                      |
        +-------------------------+--------------------------------------------------------+
        | client_version          | The version of the client being used                   |
        +-------------------------+--------------------------------------------------------+
        | client_metatag          | Any additional information (ex. email address of user) |
        +-------------------------+--------------------------------------------------------+
        | http_proxy              | http proxy being used - http(s)://user:pwd@{ip}:{port} |
        +-------------------------+--------------------------------------------------------+
        | https_proxy             | https proxy being used - http(s)://user:pwd@{ip}:{port}|
        +-------------------------+--------------------------------------------------------+

        :param dict config: A dictionary of configuration options.
        """
        # set properties
        self.auth = config.get(TruSTARConfig.AUTH.value)
        self.base = config.get(TruSTARConfig.BASE.value)
        self.station = config.get(TruSTARConfig.STATION.value)
        self.api_key = config.get(TruSTARConfig.API_KEY.value)
        self.api_secret = config.get(TruSTARConfig.API_SECRET.value)
        self.client_type = config.get(TruSTARConfig.CLIENT_TYPE.value)
        self.client_version = config.get(TruSTARConfig.CLIENT_VERSION.value)
        self.client_metatag = config.get(TruSTARConfig.CLIENT_METATAG.value)
        self.verify = config.get(TruSTARConfig.VERIFY.value)
        self.retry = config.get(TruSTARConfig.RETRY.value)
        self.max_wait_time = config.get(TruSTARConfig.MAX_WAIT_TIME.value)

        # To support proxy
        self.proxies = {}
        if config.get(TruSTARConfig.HTTP_PROXY.value):
            self.proxies[TruSTARConfig.HTTP.value] = config.get(TruSTARConfig.HTTP_PROXY.value)

        if config.get(TruSTARConfig.HTTPS_PROXY.value):
            self.proxies[TruSTARConfig.HTTPS.value] = config.get(TruSTARConfig.HTTPS_PROXY.value)

        # initialize token property
        self.token = None
        # initialize last_response property
        self.last_response = None

    def _get_token(self):
        """
        Returns the token.  If no token has been generated yet, gets one first.
        :return: The OAuth2 token.
        """
        if not self.token:
            self._refresh_token()
        return self.token

    def _refresh_token(self):
        """
        Retrieves the OAuth2 token generated by the user's API key and API secret.
        Sets the instance property 'token' to this new token.
        If the current token is still live, the server will simply return that.
        """
        # use basic auth with API key and secret
        client_auth = requests.auth.HTTPBasicAuth(self.api_key, self.api_secret)

        # make request
        post_data = {TSAuth.GRANT_TYPE.value: TSAuth.CLIENT_CREDENTIALS.value}

        response = requests.post(self.auth,
                                 auth=client_auth,
                                 data=post_data,
                                 verify=self.verify,
                                 proxies=self.proxies)
        self.last_response = response

        # raise exception if status code indicates an error
        if 400 <= response.status_code < 600:
            error_cause = CLIENT if response.status_code < 500 else SERVER
            message = (f"{response.status_code} {error_cause} Error "
                       f"(Trace-Id: {self._get_trace_id(response)}): unable to get token")
            raise HTTPError(message, response=response)

        # set token property to the received token
        self.token = response.json().get(TSAuth.ACCESS_TOKEN.value)

    def _get_headers(self, is_json=False):
        """
        Creates headers dictionary for a request.

        :param boolean is_json: Whether the request body is a json.
        :return: The headers dictionary.
        """
        headers = {TSAuth.AUTHZ.value: f"Bearer {self._get_token()}"}

        if self.client_metatag:
            headers[TSAuth.CLIENT_METATAG.value] = self.client_metatag

        if self.client_type:
            headers[TSAuth.CLIENT_TYPE.value] = self.client_type

        if self.client_version:
            headers[TSAuth.CLIENT_VERSION.value] = self.client_version

        if is_json:
            headers[TSAuth.CONTENT_TYPE.value] = TSAuth.APP_JSON.value

        return headers

    @classmethod
    def _is_expired_token_response(cls, response):
        """
        Determines whether the given response indicates that the token is expired.

        :param response: The response object.
        :return: True if the response indicates that the token is expired.
        """
        expired_message = "Expired oauth2 access token"
        invalid_message = "Invalid oauth2 access token"
        error_messages = (expired_message, invalid_message)

        if response.status_code == 400:
            try:
                body = response.json()
                if f"{body.get(TSError.ERROR_DESCRIPTION.value, None)}" in error_messages:
                    return True
            except json.decoder.JSONDecodeError:
                logger.exception("Failed to parse response for API token")

        return False

    def request(self, method, path, headers=None, params=None,
                data=None, **kwargs):
        """
        A wrapper around `requests.request` that handles boilerplate code
        specific to TS API.

        :param method: The method of the request (`GET`, `PUT`, `POST`, or `DELETE`)
        :param path: The path of the request, i.e. the piece of the URL after the
            base URL
        :param headers: A dictionary to be merged with the base headers for the SDK
        :param kwargs: Any extra keyword arguments. Forwarded to the call to
            `requests.request`
        :return: The response object.
        """
        attempted = False
        reason = "unknown cause"
        retry = self.retry

        while not attempted or retry:

            # get headers and merge with headers from method parameter if it exists
            base_headers = self._get_headers(is_json=method in ("POST", "PUT"))
            if headers:
                base_headers.update(headers)

            url = f"{self.base}/{path}"

            # make request
            response = requests.request(method=method,
                                        url=url,
                                        headers=base_headers,
                                        verify=self.verify,
                                        params=params,
                                        data=data,
                                        proxies=self.proxies,
                                        **kwargs)
            self.last_response = response
            attempted = True

            # log request
            logger.debug("%s %s. Trace-Id: %s. Params: %s",
                         method, url, response.headers.get('Trace-Id'), params)

            # refresh token if expired
            if self._is_expired_token_response(response):
                self._refresh_token()
            elif retry and response.status_code == 429:
                # if "too many requests" status code received, wait until next request
                # will be allowed and retry
                wait_time = ceil(response.json().get(TSResponse.WAIT_TIME.value) / 1000)
                logger.debug("Waiting %d seconds until next request allowed", wait_time)

                # if wait time exceeds max wait time, allow the exception to be thrown
                if wait_time <= self.max_wait_time:
                    time.sleep(wait_time)
                else:
                    retry = False
            else:
                # request cycle is complete
                retry = False

        # raise exception if status code indicates an error
        if 400 <= response.status_code < 600:
            # get response json body, if one exists
            resp_json = None
            try:
                resp_json = response.json()
            except json.decoder.JSONDecodeError:
                logger.exception("Failed to parse API response into JSON")

            # get message from json body, if one exists
            if resp_json and TSResponse.MESSAGE.value in resp_json:
                reason = resp_json.get(TSResponse.MESSAGE.value)

            # construct error message
            error_cause = CLIENT if response.status_code < 500 else SERVER
            message = (f"{response.status_code} {error_cause} Error "
                       f"(Trace-Id: {self._get_trace_id(response)}): {reason}")
            # raise HTTPError
            raise HTTPError(message, response=response)

        return response

    def get_last_trace_id(self):
        """
        The TS API responds to all requests with a header "Trace-Id",
        which contains an ID that can be correlated against all logs for a request
        across TruSTAR's platform. This method returns the trace ID for the most
        recent request made by this SDK.

        :return: The trace ID.

        .. warning:: This method is not thread-safe.
        """
        # find the last response stored in the thread context
        if self.last_response is None:
            return None

        # find the trace ID in the last response, if it exists
        return self._get_trace_id(self.last_response)

    @classmethod
    def _get_trace_id(cls, response):
        """
        Finds the trace ID in the response, if it exists
        """
        return response.headers.get('Trace-Id', None)

    def get(self, path, params=None, **kwargs):
        """
        Convenience method for making `GET` calls.

        :param str path: The path of the request, i.e. the piece of the URL after the base URL.
        :param kwargs: Any extra keyword arguments. Forwarded to the call to `requests.request`.
        :return: The response object.
        """
        return self.request("GET", path, params=params, **kwargs)

    def put(self, path, params=None, data=None, **kwargs):
        """
        Convenience method for making `PUT` calls.

        :param str path: The path of the request, i.e. the piece of the URL after the base URL.
        :param kwargs: Any extra keyword arguments. Forwarded to the call to `requests.request`.
        :return: The response object.
        """
        return self.request("PUT", path, params=params, data=data, **kwargs)

    def post(self, path, params=None, data=None, **kwargs):
        """
        Convenience method for making `POST` calls.

        :param str path: The path of the request, i.e. the piece of the URL after the base URL.
        :param kwargs: Any extra keyword arguments. Forwarded to the call to `requests.request`.
        :return: The response object.
        """
        return self.request("POST", path, params=params, data=data, **kwargs)

    def delete(self, path, params=None, **kwargs):
        """
        Convenience method for making `DELETE` calls.

        :param str path: The path of the request, i.e. the piece of the URL after the base URL.
        :param kwargs: Any extra keyword arguments. Forwarded to the call to `requests.request`.
        :return: The response object.
        """
        return self.request("DELETE", path, params=params, **kwargs)
