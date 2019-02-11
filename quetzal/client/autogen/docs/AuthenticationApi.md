# quetzal.client.autogen.AuthenticationApi

All URIs are relative to *https://api.quetz.al/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_api_auth_get_token**](AuthenticationApi.md#app_api_auth_get_token) | **POST** /auth/token | Authenticate and obtain a token
[**app_api_auth_logout**](AuthenticationApi.md#app_api_auth_logout) | **POST** /auth/logout | Logout and invalidate the existing token


# **app_api_auth_get_token**
> InlineResponse200 app_api_auth_get_token()

Authenticate and obtain a token

### Example

* Basic Authentication (basic):
```python
from __future__ import print_function
import time
import quetzal.client.autogen
from quetzal.client.autogen.rest import ApiException
from pprint import pprint
configuration = quetzal.client.autogen.Configuration()
# Configure HTTP basic authorization: basic
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = quetzal.client.autogen.AuthenticationApi(quetzal.client.autogen.ApiClient(configuration))

try:
    # Authenticate and obtain a token
    api_response = api_instance.app_api_auth_get_token()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthenticationApi->app_api_auth_get_token: %s\n" % e)
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

# **app_api_auth_logout**
> app_api_auth_logout()

Logout and invalidate the existing token

### Example

* Bearer Authentication (bearer):
```python
from __future__ import print_function
import time
import quetzal.client.autogen
from quetzal.client.autogen.rest import ApiException
from pprint import pprint
configuration = quetzal.client.autogen.Configuration()
# Configure Bearer authorization: bearer
configuration.access_token = 'YOUR_BEARER_TOKEN'

# create an instance of the API class
api_instance = quetzal.client.autogen.AuthenticationApi(quetzal.client.autogen.ApiClient(configuration))

try:
    # Logout and invalidate the existing token
    api_instance.app_api_auth_logout()
except ApiException as e:
    print("Exception when calling AuthenticationApi->app_api_auth_logout: %s\n" % e)
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

