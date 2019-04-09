import functools
import io
import logging
import re
import textwrap
import urllib.parse
import warnings

import backoff
import six
import urllib3
from requests import codes

from quetzal.openapi_client.api_client import ApiClient
from quetzal.openapi_client.rest import RESTClientObject
from quetzal.openapi_client.api import AuthenticationApi, DataApi
from quetzal.openapi_client.rest import ApiException
from quetzal.client.exceptions import QuetzalAPIException, RetryableException

logger = logging.getLogger(__name__)

# Size of chunk for uploading data as chunked multi-part
CHUNK_SIZE = (32 << 20)  # 32 Mb


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


class CustomDataApi(DataApi):

    def workspace_file_details_with_http_info(self, wid, uuid, **kwargs):
        local_var_params = locals()

        all_params = ['wid', 'uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_accept')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method app_api_data_file_details_w" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'wid' is set
        if ('wid' not in local_var_params or
                local_var_params['wid'] is None):
            raise ValueError("Missing the required parameter `wid` when calling `workspace_file_details`")  # noqa: E501
        # verify the required parameter 'uuid' is set
        if ('uuid' not in local_var_params or
                local_var_params['uuid'] is None):
            raise ValueError("Missing the required parameter `uuid` when calling `workspace_file_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'wid' in local_var_params:
            path_params['wid'] = local_var_params['wid']  # noqa: E501
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = local_var_params.get('_accept', self.api_client.select_header_accept(
            ['application/json', 'application/octet-stream', 'application/problem+json'])  # noqa: E501
        )

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/data/workspaces/{wid}/files/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def public_file_details_with_http_info(self, uuid, **kwargs):  # noqa: E501

        local_var_params = locals()

        all_params = ['uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        all_params.append('_accept')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method app_api_data_file_details" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if ('uuid' not in local_var_params or
                local_var_params['uuid'] is None):
            raise ValueError("Missing the required parameter `uuid` when calling `app_api_data_file_details`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = local_var_params.get('_accept', self.api_client.select_header_accept(
            ['application/json', 'application/octet-stream', 'application/problem+json'])  # noqa: E501
        )

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/data/files/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)


class MetaClient(type):
    """Metaclass that converts the API operation methods to a shorter name

    This metaclass assumes that there is a `api_auth` and `api_data` member
    that have Quetzal's authentication and data API methods, respectively.
    It creates new methods named in a shorter way, by removing the `app_api_`
    prefix inherited from the `operationId` in the OpenAPI specification.

    """

    def __new__(cls, name, bases, dct):
        # Create the class
        obj = super().__new__(cls, name, bases, dct)
        # Force the creation of some attributes (this could be handled in a better way)
        setattr(obj, 'api_auth', None)
        setattr(obj, 'api_data', None)
        # Make shortcut methods
        MetaClient.make_shortcuts(obj, AuthenticationApi,
                                  'auth_api', 'auth')
        MetaClient.make_shortcuts(obj, CustomDataApi,
                                  'data_api', 'workspace')
        MetaClient.make_shortcuts(obj, CustomDataApi,
                                  'data_api', 'public')
        return obj

    @staticmethod
    def make_shortcuts(obj, api_obj, api_property, prefix):
        for attr in dir(api_obj):
            if not attr.startswith(prefix) or attr.endswith('_with_http_info'):
                continue

            def wrapper(f):
                @functools.wraps(f)
                def shortcut(self, *args, **kwargs):
                    instance = getattr(self, api_property)
                    return f(instance, *args, **kwargs)
                return shortcut

            original_doc = '\n'.join(line.strip()
                                     for line in getattr(api_obj, attr).__doc__.split('\n'))
            short_func = wrapper(getattr(api_obj, attr))
            short_func.__doc__ = textwrap.dedent(
                f'Shortcut method for {api_obj.__module__}.{api_obj.__name__}.{attr}\n\n'
                f'Original docstring:\n{original_doc}'
            )
            logger.debug('Setting shortcut method in %s: %s -> %s', obj.__name__, attr, attr)
            setattr(obj, attr, short_func)


class Client(ApiClient, metaclass=MetaClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_api = AuthenticationApi(self)
        self._data_api = CustomDataApi(self)
        self.default_headers['Cache-Control'] = 'no-cache'
        self.rest_client = CustomRestClient(self.configuration)

    @property
    def auth_api(self):
        return self._auth_api

    @property
    def data_api(self):
        return self._data_api

    @_auth_retry_decorator
    def call_api(self, *args, **kwargs):
        # Patch for query create. The openapi-generator incorrectly assumes that
        # its response type is an ProblemType
        resource_path = args[0] if args else None
        method = args[1] if args else None
        if resource_path == '/data/workspaces/{wid}/queries/' and method == 'POST':
            kwargs['response_type'] = 'Query'

        # Patch in to login with basic authentication before trying a
        # bearer-protected endpoint
        auth_settings = kwargs.get('auth_settings', None)
        if auth_settings == ['bearer'] and not self.configuration.access_token:
            logger.debug('Trying to access an endpoint with bearer authentication, '
                         'but there is no saved access_token. Logging in...')
            self.login()

        # Call the api, but check for 401 errors that may be retried with the
        # correct authentication; that is, by doing a login again because the
        # token may be outdated
        try:
            return super().call_api(*args, **kwargs)
        except ApiException as api_ex:
            may_retry_to_authorize = (resource_path != '/auth/token')
            raise QuetzalAPIException.from_api_exception(api_ex, authorize_ok=may_retry_to_authorize) from api_ex
        except urllib3.exceptions.MaxRetryError as ex:
            if isinstance(ex.reason, urllib3.exceptions.SSLError):
                warnings.warn('Got SSLError when calling the API. Set the '
                              'insecure option if you are using a local '
                              'https server', UserWarning)
            raise

    @property
    def can_login(self):
        return self.configuration.username and self.configuration.password

    def login(self):
        if not self.can_login:
            return
        response = self.auth_get_token()
        self.configuration.access_token = response.token


class CustomRestClient(RESTClientObject):

    def __init__(self, configuration, pools_size=4, maxsize=None):
        super().__init__(configuration, pools_size, maxsize)

        # override https pool manager
        if configuration.proxy:
            self.pool_manager = CustomProxyManager(
                num_pools=pools_size,
                **self.pool_manager.connection_pool_kw
            )
        else:
            self.pool_manager = CustomPoolManager(
                num_pools=pools_size,
                **self.pool_manager.connection_pool_kw
            )


class CustomPoolManager(urllib3.PoolManager):

    def urlopen(self, method, url, redirect=True, **kw):
        kw = _patch_urlopen_keywords(method, url, redirect, kw)
        return super().urlopen(method, url, redirect, **kw)


class CustomProxyManager(urllib3.ProxyManager):

    def urlopen(self, method, url, redirect=True, **kw):
        kw = _patch_urlopen_keywords(method, url, redirect, kw)
        return super().urlopen(method, url, redirect, **kw)


def _patch_urlopen_keywords(method, url, redirect, kw):
    """urlopen patch to follow 303 responses and keep the Authorization header"""
    path = urllib.parse.urlparse(url).path
    if method == 'POST' and re.match('^/api/v1/data/(?:workspaces/[0-9]*/)?queries/?$', path):
        # Patch 303 retry strategy for queries, inside or outside a workspace
        retries = kw.get('retries')
        if not isinstance(retries, urllib3.util.retry.Retry):
            retries = urllib3.util.retry.Retry.from_int(retries, redirect=redirect)
        retries.remove_headers_on_redirect = ()
        kw['retries'] = retries
    elif method == 'POST' and re.match('^/api/v1/data/workspaces/[0-9]*/files/$', path):
        # Patch 303 retry strategy for file upload
        kw['chunked'] = True
        kw['body'] = _chunked_body_generator(kw.pop('body'))
    return kw


def _chunked_body_generator(data):
    foo = io.BytesIO(data)
    chunk = foo.read(CHUNK_SIZE)
    n = len(data)
    # import tqdm
    # progress = tqdm.tqdm('Uploading file', total=n, unit='bytes')
    while chunk:
        # progress.update(len(chunk))
        yield chunk
        chunk = foo.read(CHUNK_SIZE)
    # progress.clear()
    # print('Finished uploading?')

