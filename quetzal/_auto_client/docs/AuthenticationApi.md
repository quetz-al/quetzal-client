# quetzal._auto_client.AuthenticationApi

All URIs are relative to *https://api.quetz.al/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_get_token**](AuthenticationApi.md#auth_get_token) | **POST** /auth/token | Login.
[**auth_logout**](AuthenticationApi.md#auth_logout) | **POST** /auth/logout | Logout.


# **auth_get_token**
> InlineResponse200 auth_get_token()

Login.

Authenticate with simple HTTP authentication and obtain a bearer token. This bearer token can be used on the other endpoints of the API.

### Example

* Basic Authentication (basic):
```python
from __future__ import print_function
import time
import quetzal._auto_client
from quetzal._auto_client.rest import ApiException
from pprint import pprint
configuration = quetzal._auto_client.Configuration()
# Configure HTTP basic authorization: basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = quetzal._auto_client.AuthenticationApi(quetzal._auto_client.ApiClient(configuration))

try:
    # Login.
    api_response = api_instance.auth_get_token()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthenticationApi->auth_get_token: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[basic](../README.md#basic)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_logout**
> auth_logout()

Logout.

Logout by invalidating the existing token.

### Example

* Bearer Authentication (bearer):
```python
from __future__ import print_function
import time
import quetzal._auto_client
from quetzal._auto_client.rest import ApiException
from pprint import pprint
configuration = quetzal._auto_client.Configuration()
# Configure Bearer authorization: bearer
configuration.access_token = 'YOUR_BEARER_TOKEN'

# create an instance of the API class
api_instance = quetzal._auto_client.AuthenticationApi(quetzal._auto_client.ApiClient(configuration))

try:
    # Logout.
    api_instance.auth_logout()
except ApiException as e:
    print("Exception when calling AuthenticationApi->auth_logout: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

