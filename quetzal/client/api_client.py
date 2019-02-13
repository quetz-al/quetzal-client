import logging

import backoff

import quetzal.client.autogen
import quetzal.client.autogen.rest


logger = logging.getLogger(__name__)


class UnauthorizedException(Exception):
    pass


def _log_auth_backoff(details):
    print("Backing off {wait:0.1f} seconds afters {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))


def _retry_login(details):
    args = details['args']
    client = args[0]
    try:
        client.login()
    except:
        print('Could not login')


def _fatal_code(e):
    # if e.status_code < 400:
    #     return False
    # elif e.status_code < 500:
    #     return e.status_code not in (401, 403, )
    # pass
    # ???????
    return e.status == 500


_auth_retry_decorator = backoff.on_exception(
    backoff.expo,
    quetzal.client.autogen.rest.ApiException,
    max_tries=3,
    giveup=_fatal_code,
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
            if api_ex.status == 401 and resource_path == '/auth/token':
                # Do not retry if this is an authentication attempt and it
                # failed from invalid credentials
                raise UnauthorizedException from api_ex
            else:
                raise

    @property
    def can_login(self):
        return self.configuration.username and self.configuration.password

    def login(self):
        if not self.can_login:
            return
        response = self.auth_api.app_api_auth_get_token()
        self.configuration.access_token = response.token
