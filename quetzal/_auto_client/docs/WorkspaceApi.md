# quetzal._auto_client.WorkspaceApi

All URIs are relative to *https://api.quetz.al/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**workspace_commit**](WorkspaceApi.md#workspace_commit) | **PUT** /data/workspaces/{wid}/commit | Commit workspace.
[**workspace_details**](WorkspaceApi.md#workspace_details) | **GET** /data/workspaces/{wid} | Workspace details.
[**workspace_fetch**](WorkspaceApi.md#workspace_fetch) | **GET** /data/workspaces/ | List workspaces.
[**workspace_file_create**](WorkspaceApi.md#workspace_file_create) | **POST** /data/workspaces/{wid}/files/ | Upload file.
[**workspace_file_details**](WorkspaceApi.md#workspace_file_details) | **GET** /data/workspaces/{wid}/files/{uuid} | Fetch file.
[**workspace_file_fetch**](WorkspaceApi.md#workspace_file_fetch) | **GET** /data/workspaces/{wid}/files/ | List files.
[**workspace_file_set_metadata**](WorkspaceApi.md#workspace_file_set_metadata) | **PUT** /data/workspaces/{wid}/files/{uuid} | Rewrite metadata.
[**workspace_file_update_metadata**](WorkspaceApi.md#workspace_file_update_metadata) | **PATCH** /data/workspaces/{wid}/files/{uuid} | Modify metadata.
[**workspace_query_create**](WorkspaceApi.md#workspace_query_create) | **POST** /data/workspaces/{wid}/queries/ | Prepare a query.
[**workspace_query_details**](WorkspaceApi.md#workspace_query_details) | **GET** /data/workspaces/{wid}/queries/{qid} | Query details.
[**workspace_query_fetch**](WorkspaceApi.md#workspace_query_fetch) | **GET** /data/workspaces/{wid}/queries/ | List queries.
[**workspace_scan**](WorkspaceApi.md#workspace_scan) | **PUT** /data/workspaces/{wid}/scan | Update views.


# **workspace_commit**
> InlineResponse2001Results workspace_commit(wid)

Commit workspace.

Requests a workspace commit. That is, all metadata added or modified in this workspace will be moved to the global, public workspace, becoming available to all users. Metadata versions will be incremented.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Commit workspace.
    api_response = api_instance.workspace_commit(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_commit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**InlineResponse2001Results**](InlineResponse2001Results.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_details**
> InlineResponse2001Results workspace_details(wid)

Workspace details.

Obtain all information of a workspace.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Workspace details.
    api_response = api_instance.workspace_details(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**InlineResponse2001Results**](InlineResponse2001Results.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_fetch**
> InlineResponse2001 workspace_fetch(page=page, per_page=per_page, name=name, owner=owner, deleted=deleted)

List workspaces.

List workspace details. Optionally, filter workspaces according to their name, owner or whether they have been deleted.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)
name = 'name_example' # str | Filter workspaces by name (optional)
owner = 'owner_example' # str | Filter workspaces by owner (optional)
deleted = True # bool | Include deleted workspaces (optional)

try:
    # List workspaces.
    api_response = api_instance.workspace_fetch(page=page, per_page=per_page, name=name, owner=owner, deleted=deleted)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]
 **name** | **str**| Filter workspaces by name | [optional] 
 **owner** | **str**| Filter workspaces by owner | [optional] 
 **deleted** | **bool**| Include deleted workspaces | [optional] 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_create**
> InlineResponse2002Results workspace_file_create(wid, file_content=file_content)

Upload file.

Upload a new file to a workspace by sending its contents. The file will not have any additional metadata associated to it.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
file_content = '/path/to/file' # file |  (optional)

try:
    # Upload file.
    api_response = api_instance.workspace_file_create(wid, file_content=file_content)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_file_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **file_content** | **file**|  | [optional] 

### Return type

[**InlineResponse2002Results**](InlineResponse2002Results.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_details**
> InlineResponse2003 workspace_file_details(wid, uuid)

Fetch file.

Serves the file contents or its metadata, according to the accepted content response header. When the metadata is requested, this returns the updated version with the modifications that may have been introduced in this workspace.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier

try:
    # Fetch file.
    api_response = api_instance.workspace_file_details(wid, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_file_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_fetch**
> InlineResponse2002 workspace_file_fetch(wid, page=page, per_page=per_page, filters=filters)

List files.

Fetches all the files that have been added in this workspace. Files whose metadata has been modified in this workspace will also be included.  The file details included in the response only show their base metadata.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)
filters = filename=foo.png,path=images,size=12314 # str | Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. (optional)

try:
    # List files.
    api_response = api_instance.workspace_file_fetch(wid, page=page, per_page=per_page, filters=filters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_file_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]
 **filters** | **str**| Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. | [optional] 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_set_metadata**
> InlineResponse2003 workspace_file_set_metadata(wid, uuid, inline_object2=inline_object2)

Rewrite metadata.

Change the file metadata entirely. In contrast to the PATCH method to on this endpoint, this method sets the new metadata and discards any previous metadata that was defined before.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier
inline_object2 = quetzal._auto_client.InlineObject2() # InlineObject2 |  (optional)

try:
    # Rewrite metadata.
    api_response = api_instance.workspace_file_set_metadata(wid, uuid, inline_object2=inline_object2)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_file_set_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 
 **inline_object2** | [**InlineObject2**](InlineObject2.md)|  | [optional] 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_update_metadata**
> InlineResponse2003 workspace_file_update_metadata(wid, uuid, inline_object3=inline_object3)

Modify metadata.

Change the file metadata by updating it. Updating metadata changes key/value pairs, adding a new key/value pair if does not exist and changing the value if the key already exists. However, it cannot delete a key/value that already exists. To delete metadata, refer to the PUT method on this endpoint.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier
inline_object3 = quetzal._auto_client.InlineObject3() # InlineObject3 |  (optional)

try:
    # Modify metadata.
    api_response = api_instance.workspace_file_update_metadata(wid, uuid, inline_object3=inline_object3)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_file_update_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 
 **inline_object3** | [**InlineObject3**](InlineObject3.md)|  | [optional] 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_create**
> InlineResponse201 workspace_query_create(wid, inline_object4, page=page, per_page=per_page)

Prepare a query.

Queries in Quetzal are saved as a resource associated to a workspace. This endpoint creates one and responds with a _see other_ status referencing the query details endpoint.  Since the query details contains the query results as a paginated list, this endpoint also accepts the normal pagination parameters.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
inline_object4 = quetzal._auto_client.InlineObject4() # InlineObject4 | 
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # Prepare a query.
    api_response = api_instance.workspace_query_create(wid, inline_object4, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_query_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **inline_object4** | [**InlineObject4**](InlineObject4.md)|  | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**InlineResponse201**](InlineResponse201.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_details**
> InlineResponse201 workspace_query_details(wid, qid, page=page, per_page=per_page)

Query details.

The details of a query, which contains the query itself and a paginated list of its results.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
qid = 56 # int | Query identifier
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # Query details.
    api_response = api_instance.workspace_query_details(wid, qid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_query_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **qid** | **int**| Query identifier | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**InlineResponse201**](InlineResponse201.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_fetch**
> InlineResponse2004 workspace_query_fetch(wid, page=page, per_page=per_page)

List queries.

List all the queries that are associated with a workspace. Note that each query listed here is shown _without_ its results, for brevity.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # List queries.
    api_response = api_instance.workspace_query_fetch(wid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_query_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_scan**
> InlineResponse2001Results workspace_scan(wid)

Update views.

Requests the update of the views of a workspace. All the internal databases used for the query operation will be updated to contain the latest modifications of the metadata.

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
api_instance = quetzal._auto_client.WorkspaceApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Update views.
    api_response = api_instance.workspace_scan(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkspaceApi->workspace_scan: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**InlineResponse2001Results**](InlineResponse2001Results.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

