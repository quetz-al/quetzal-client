# quetzal.client.autogen.DataApi

All URIs are relative to *https://api.quetz.al/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**app_api_data_file_create**](DataApi.md#app_api_data_file_create) | **POST** /data/workspaces/{wid}/files/ | Add a new file
[**app_api_data_file_details**](DataApi.md#app_api_data_file_details) | **GET** /data/files/{uuid} | Fetch file metadata or contents
[**app_api_data_file_details_w**](DataApi.md#app_api_data_file_details_w) | **GET** /data/workspaces/{wid}/files/{uuid} | Fetch file metadata or contents
[**app_api_data_file_fetch**](DataApi.md#app_api_data_file_fetch) | **GET** /data/workspaces/{wid}/files/ | List workspace files
[**app_api_data_file_set_metadata**](DataApi.md#app_api_data_file_set_metadata) | **PUT** /data/workspaces/{wid}/files/{uuid} | Rewrite file metadata
[**app_api_data_file_update_metadata**](DataApi.md#app_api_data_file_update_metadata) | **PATCH** /data/workspaces/{wid}/files/{uuid} | Modify file metadata
[**app_api_data_query_create**](DataApi.md#app_api_data_query_create) | **POST** /data/workspaces/{wid}/queries/ | Prepare a query for a workspace
[**app_api_data_query_details**](DataApi.md#app_api_data_query_details) | **GET** /data/workspaces/{wid}/queries/{qid} | Get details on query
[**app_api_data_query_fetch**](DataApi.md#app_api_data_query_fetch) | **GET** /data/workspaces/{wid}/queries/ | List all queries of a workspace
[**app_api_data_workspace_commit**](DataApi.md#app_api_data_workspace_commit) | **PUT** /data/workspaces/{wid}/commit | Commit a workspace
[**app_api_data_workspace_create**](DataApi.md#app_api_data_workspace_create) | **POST** /data/workspaces/ | Create a new workspace
[**app_api_data_workspace_delete**](DataApi.md#app_api_data_workspace_delete) | **DELETE** /data/workspaces/{wid} | Request deletion of a workspace
[**app_api_data_workspace_details**](DataApi.md#app_api_data_workspace_details) | **GET** /data/workspaces/{wid} | Workspace details
[**app_api_data_workspace_fetch**](DataApi.md#app_api_data_workspace_fetch) | **GET** /data/workspaces/ | Get all workspaces
[**app_api_data_workspace_scan**](DataApi.md#app_api_data_workspace_scan) | **PUT** /data/workspaces/{wid}/scan | Update workspace views


# **app_api_data_file_create**
> object app_api_data_file_create(wid, file_content=file_content)

Add a new file

Upload a new file by sending its contents. The file will not have any additional metadata associated to it.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
file_content = '/path/to/file' # file |  (optional)

try:
    # Add a new file
    api_response = api_instance.app_api_data_file_create(wid, file_content=file_content)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **file_content** | **file**|  | [optional] 

### Return type

**object**

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_file_details**
> object app_api_data_file_details(uuid)

Fetch file metadata or contents

Serves the file contents or its metadata, according to the accepted content response header. In the case of metadata, this endpoint returns the most recent metadata that has been committed.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
uuid = 'uuid_example' # str | File identifier

try:
    # Fetch file metadata or contents
    api_response = api_instance.app_api_data_file_details(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| File identifier | 

### Return type

**object**

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_file_details_w**
> object app_api_data_file_details_w(wid, uuid)

Fetch file metadata or contents

Serves the file contents or its metadata, according to the accepted content response header. When the metadata is requested, this returns the updated version with the modifications that may have been introduced in this workspace.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
uuid = 'uuid_example' # str | File identifier

try:
    # Fetch file metadata or contents
    api_response = api_instance.app_api_data_file_details_w(wid, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_details_w: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **uuid** | [**str**](.md)| File identifier | 

### Return type

**object**

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_file_fetch**
> InlineResponse2002 app_api_data_file_fetch(wid, page=page, per_page=per_page)

List workspace files

Fetchs all the files that have been added in this workspace. Files whose metadata has been modified in this workspace will also be included.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # List workspace files
    api_response = api_instance.app_api_data_file_fetch(wid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_file_set_metadata**
> object app_api_data_file_set_metadata(wid, uuid, body=body)

Rewrite file metadata

Change the file metadata entirely. In contrast to the PATCH method to on this endpoint, this method sets the new metadata and discards any previous metadata that was defined before.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
uuid = 'uuid_example' # str | File identifier
body = NULL # object |  (optional)

try:
    # Rewrite file metadata
    api_response = api_instance.app_api_data_file_set_metadata(wid, uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_set_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **uuid** | [**str**](.md)| File identifier | 
 **body** | **object**|  | [optional] 

### Return type

**object**

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_file_update_metadata**
> object app_api_data_file_update_metadata(wid, uuid, body=body)

Modify file metadata

Change the file metadata by updating it. Updating metadata changes key/value pairs, adding a new key/value pair if does not exist and changing the value if the key already exists. However, it cannot delete a key/value that already exists. To delete metadata, refer to the PUT method on this endpoint.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
uuid = 'uuid_example' # str | File identifier
body = NULL # object |  (optional)

try:
    # Modify file metadata
    api_response = api_instance.app_api_data_file_update_metadata(wid, uuid, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_file_update_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **uuid** | [**str**](.md)| File identifier | 
 **body** | **object**|  | [optional] 

### Return type

**object**

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_query_create**
> InlineResponseDefault app_api_data_query_create(wid, metadata_query_type1)

Prepare a query for a workspace

Description

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
metadata_query_type1 = quetzal.client.autogen.MetadataQueryType1() # MetadataQueryType1 | 

try:
    # Prepare a query for a workspace
    api_response = api_instance.app_api_data_query_create(wid, metadata_query_type1)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_query_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **metadata_query_type1** | [**MetadataQueryType1**](MetadataQueryType1.md)|  | 

### Return type

[**InlineResponseDefault**](InlineResponseDefault.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_query_details**
> MetadataQueryType app_api_data_query_details(wid, qid, page=page, per_page=per_page)

Get details on query

Description.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
qid = 56 # int | Query identifier
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # Get details on query
    api_response = api_instance.app_api_data_query_details(wid, qid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_query_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **qid** | **int**| Query identifier | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**MetadataQueryType**](MetadataQueryType.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_query_fetch**
> InlineResponse2003 app_api_data_query_fetch(wid, page=page, per_page=per_page)

List all queries of a workspace

List all the queries that are associated with a workspace.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # List all queries of a workspace
    api_response = api_instance.app_api_data_query_fetch(wid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_query_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_workspace_commit**
> WorkspaceDetailsType app_api_data_workspace_commit(wid)

Commit a workspace

Requests a workspace commit. That is, all metadata added or modified in this workspace will be committed to the global workspace, becoming available to all users. Metadata versions will be incremented.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier

try:
    # Commit a workspace
    api_response = api_instance.app_api_data_workspace_commit(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_commit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 

### Return type

[**WorkspaceDetailsType**](WorkspaceDetailsType.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_workspace_create**
> WorkspaceDetailsType app_api_data_workspace_create(workspace_details_type1)

Create a new workspace

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
workspace_details_type1 = quetzal.client.autogen.WorkspaceDetailsType1() # WorkspaceDetailsType1 | 

try:
    # Create a new workspace
    api_response = api_instance.app_api_data_workspace_create(workspace_details_type1)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_details_type1** | [**WorkspaceDetailsType1**](WorkspaceDetailsType1.md)|  | 

### Return type

[**WorkspaceDetailsType**](WorkspaceDetailsType.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_workspace_delete**
> app_api_data_workspace_delete(wid)

Request deletion of a workspace

Marks a workspace for deletion. Workspaces cannot be immediately deleted, due to complex resource management. The status of the workspace can be requested on this same path, using a GET instead of a DELETE.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier

try:
    # Request deletion of a workspace
    api_instance.app_api_data_workspace_delete(wid)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 

### Return type

void (empty response body)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_workspace_details**
> WorkspaceDetailsType app_api_data_workspace_details(wid)

Workspace details

Fetchs all details of a workspace

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier

try:
    # Workspace details
    api_response = api_instance.app_api_data_workspace_details(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 

### Return type

[**WorkspaceDetailsType**](WorkspaceDetailsType.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **app_api_data_workspace_fetch**
> InlineResponse2001 app_api_data_workspace_fetch(page=page, per_page=per_page, name=name, owner=owner, deleted=deleted)

Get all workspaces

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)
name = 'name_example' # str | Filter workspaces by name (optional)
owner = 'owner_example' # str | Filter workspaces by owner (optional)
deleted = True # bool | Include deleted workspaces (optional)

try:
    # Get all workspaces
    api_response = api_instance.app_api_data_workspace_fetch(page=page, per_page=per_page, name=name, owner=owner, deleted=deleted)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_fetch: %s\n" % e)
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

# **app_api_data_workspace_scan**
> WorkspaceDetailsType app_api_data_workspace_scan(wid)

Update workspace views

Requests the update of the views of a workspace. All the internal databases used for the query operation will be updated to contain the latest modifications of the metadata.

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
api_instance = quetzal.client.autogen.DataApi(quetzal.client.autogen.ApiClient(configuration))
wid = 56 # int | Workspace identifier

try:
    # Update workspace views
    api_response = api_instance.app_api_data_workspace_scan(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->app_api_data_workspace_scan: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier | 

### Return type

[**WorkspaceDetailsType**](WorkspaceDetailsType.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

