import collections
import uuid

import pytest

from quetzal.client import helpers
from quetzal.client.exceptions import QuetzalAPIException
from quetzal.openapi_client.rest import ApiException


@pytest.fixture(scope='function')
def mocked_auth(mocker):
    login_response = collections.namedtuple('_fake_response', ['token'])
    mocked_func = mocker.patch(
        'quetzal.client.base.Client.auth_get_token',
        return_value=login_response('fake_token')
    )
    return mocked_func


@pytest.mark.usefixtures('mocked_auth')
def test_server_unavailable_retry(mocker):
    side_effects = [
        ApiException(503, f'Server unavailable, iteration {i}')
        for i in range(1, 6)
    ]
    side_effects.append({
        'metadata': {}
    })
    call_api_mock = mocker.patch('quetzal.openapi_client.api_client.ApiClient.call_api',
                                 side_effect=side_effects)

    client = helpers.get_client('https://localhost/api/v1', username='foo', password='bar')
    file_id = str(uuid.uuid4())

    helpers.file.metadata(client=client, file_id=file_id, wid=None)

    assert call_api_mock.call_count == len(side_effects)


@pytest.mark.usefixtures('mocked_auth')
def test_server_error_no_retry(mocker):
    call_api_mock = mocker.patch('quetzal.openapi_client.api_client.ApiClient.call_api',
                                 side_effect=ApiException(500, 'Server error'))

    client = helpers.get_client('https://localhost/api/v1', username='foo', password='bar')
    file_id = str(uuid.uuid4())
    with pytest.raises(QuetzalAPIException):
        helpers.file.metadata(client=client, file_id=file_id, wid=None)

    assert call_api_mock.call_count == 1


def test_auth_retry(mocker):
    call_api_mock = mocker.patch('quetzal.openapi_client.api_client.ApiClient.call_api',
                                 side_effect=ApiException(401, 'Unauthorized'))

    client = helpers.get_client('https://localhost/api/v1')
    file_id = str(uuid.uuid4())

    with pytest.raises(QuetzalAPIException):
        helpers.file.metadata(client=client, file_id=file_id, wid=None)

    assert call_api_mock.call_count >= 10


