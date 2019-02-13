import logging

import backoff
from requests import codes

import quetzal.client.autogen
import quetzal.client.autogen.rest
from quetzal.client.exceptions import QuetzalAPIException, RetryableException

logger = logging.getLogger(__name__)


def _log_auth_backoff(details):
    args = details['args']
    print('Calling function {name} ({verb} {path}) failed after {tries} tries, '
          'waiting {wait:0.1f} seconds before retrying again.'
          .format(name=details["target"].__name__, verb=args[2],
                  path=args[1], **details))


def _retry_login(details):
    print('Refreshing access token...')
    args = details['args']
    client = args[0]
    try:
        client.login()
    except:
        print('Could not login')


def _should_giveup(e):
    if isinstance(e, RetryableException):
        if e.status == codes.unauthorized:
            print('Retrying due to unauthorized error')
        return False
    return True


_auth_retry_decorator = backoff.on_exception(
    backoff.expo,
    RetryableException,
    max_tries=3,
    giveup=_should_giveup,
    on_backoff=[_log_auth_backoff, _retry_login],
)


class Client(quetzal.client.autogen.api_client.ApiClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_api = quetzal.client.autogen.api.AuthenticationApi(self)
        self._data_api = quetzal.client.autogen.api.DataApi(self)

    @property
    def auth_api(self):
        return self._auth_api

    @property
    def data_api(self):
        return self._data_api

    @_auth_retry_decorator
    def call_api(self, *args, **kwargs):
        resource_path = args[0] if args else None
        try:
            return super().call_api(*args, **kwargs)
        except quetzal.client.autogen.rest.ApiException as api_ex:
            may_retry_to_authorize = (resource_path != '/auth/token')
            raise QuetzalAPIException.from_api_exception(api_ex, authorize_ok=may_retry_to_authorize) from api_ex

    @property
    def can_login(self):
        return self.configuration.username and self.configuration.password

    def login(self):
        if not self.can_login:
            return
        response = self.auth_api.app_api_auth_get_token()
        self.configuration.access_token = response.token
