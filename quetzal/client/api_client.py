import functools
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


class MetaClient(type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)
        auth_api_obj = quetzal.client.autogen.api.AuthenticationApi
        for attr in dir(auth_api_obj):
            if attr.startswith('app_api_auth') and not attr.endswith('_with_http_info'):
                short_name = attr.replace('app_api_auth', 'auth', 1)
                func = functools.partialmethod(_auth_shortcut, 'auth_api', attr)
                func = functools.update_wrapper(func, getattr(auth_api_obj, attr))
                #print(f'{short_name} -> {attr}')
                setattr(obj, short_name, func)

        data_api_obj = quetzal.client.autogen.api.DataApi
        for attr in dir(data_api_obj):
            if attr.startswith('app_api_data') and not attr.endswith('_with_http_info'):
                short_name = attr.replace('app_api_data', 'data', 1)
                func = functools.partialmethod(_auth_shortcut, 'data_api', attr)
                func = functools.update_wrapper(func, getattr(data_api_obj, attr))
                #print(f'{short_name} -> {attr}')
                setattr(obj, short_name, func)

        return obj


def _auth_shortcut(*args, **kwargs):
    assert len(args) >= 3
    client = args[0]
    prop = args[1]
    method = args[2]
    args = args[3:]
    func = getattr(getattr(client, prop), method)
    return func(*args, **kwargs)


class Client(quetzal.client.autogen.api_client.ApiClient, metaclass=MetaClient):

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
