# quetzal._auto_client.DataApi

All URIs are relative to *https://api.quetz.al/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**public_file_details**](DataApi.md#public_file_details) | **GET** /data/files/{uuid} | Fetch public file.
[**public_file_fetch**](DataApi.md#public_file_fetch) | **GET** /data/files/ | List public files.
[**workspace_commit**](DataApi.md#workspace_commit) | **PUT** /data/workspaces/{wid}/commit | Commit workspace.
[**workspace_create**](DataApi.md#workspace_create) | **POST** /data/workspaces/ | Create workspace.
[**workspace_delete**](DataApi.md#workspace_delete) | **DELETE** /data/workspaces/{wid} | Delete workspace.
[**workspace_details**](DataApi.md#workspace_details) | **GET** /data/workspaces/{wid} | Workspace details.
[**workspace_fetch**](DataApi.md#workspace_fetch) | **GET** /data/workspaces/ | List workspaces.
[**workspace_file_create**](DataApi.md#workspace_file_create) | **POST** /data/workspaces/{wid}/files/ | Upload file.
[**workspace_file_details**](DataApi.md#workspace_file_details) | **GET** /data/workspaces/{wid}/files/{uuid} | Fetch file.
[**workspace_file_fetch**](DataApi.md#workspace_file_fetch) | **GET** /data/workspaces/{wid}/files/ | List files.
[**workspace_file_set_metadata**](DataApi.md#workspace_file_set_metadata) | **PUT** /data/workspaces/{wid}/files/{uuid} | Rewrite metadata.
[**workspace_file_update_metadata**](DataApi.md#workspace_file_update_metadata) | **PATCH** /data/workspaces/{wid}/files/{uuid} | Modify metadata.
[**workspace_query_create**](DataApi.md#workspace_query_create) | **POST** /data/workspaces/{wid}/queries/ | Prepare a query.
[**workspace_query_details**](DataApi.md#workspace_query_details) | **GET** /data/workspaces/{wid}/queries/{qid} | Query details.
[**workspace_query_fetch**](DataApi.md#workspace_query_fetch) | **GET** /data/workspaces/{wid}/queries/ | List queries.
[**workspace_scan**](DataApi.md#workspace_scan) | **PUT** /data/workspaces/{wid}/scan | Update views.


# **public_file_details**
> MetadataByFamily public_file_details(uuid)

Fetch public file.

This endpoint can be used to fetch the file contents or its metadata. The type of response, data or metadata, depends on the `Accept` request header. In the case of metadata, this endpoint returns the most recent metadata that has been committed.

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
uuid = 'uuid_example' # str | File identifier

try:
    # Fetch public file.
    api_response = api_instance.public_file_details(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->public_file_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | [**str**](.md)| File identifier | 

### Return type

[**MetadataByFamily**](MetadataByFamily.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **public_file_fetch**
> PaginatedFiles public_file_fetch(page=page, per_page=per_page, filters=filters)

List public files.

Fetches all the files that have been committed.  The file details included in the response only show their base metadata.

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)
filters = filename=foo.png,path=images,size=12314 # str | Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. (optional)

try:
    # List public files.
    api_response = api_instance.public_file_fetch(page=page, per_page=per_page, filters=filters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->public_file_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]
 **filters** | **str**| Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. | [optional] 

### Return type

[**PaginatedFiles**](PaginatedFiles.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_commit**
> Workspace workspace_commit(wid)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Commit workspace.
    api_response = api_instance.workspace_commit(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_commit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**Workspace**](Workspace.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_create**
> Workspace workspace_create(workspace)

Create workspace.

Create a workspace, which initializes the basic resources and information associated with it, and then schedules some background tasks to initialize Cloud resources.

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
workspace = quetzal._auto_client.Workspace() # Workspace | 

try:
    # Create workspace.
    api_response = api_instance.workspace_create(workspace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace** | [**Workspace**](Workspace.md)|  | 

### Return type

[**Workspace**](Workspace.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_delete**
> workspace_delete(wid)

Delete workspace.

Marks a workspace for deletion. Workspaces cannot be immediately deleted, due to complex resource management. Moreover, workspaces are not completely deleted in order to keep a history of workspaces and possibly to add some resurrect functionality. Instead, all of their resources are freed and its status is marked as DELETED.  The current status of the workspace can be requested on this same path, using a GET instead of a DELETE.

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Delete workspace.
    api_instance.workspace_delete(wid)
except ApiException as e:
    print("Exception when calling DataApi->workspace_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

void (empty response body)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_details**
> Workspace workspace_details(wid)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Workspace details.
    api_response = api_instance.workspace_details(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**Workspace**](Workspace.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_fetch**
> PaginatedWorkspaces workspace_fetch(page=page, per_page=per_page, name=name, owner=owner, deleted=deleted)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
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
    print("Exception when calling DataApi->workspace_fetch: %s\n" % e)
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

[**PaginatedWorkspaces**](PaginatedWorkspaces.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_create**
> BaseMetadata workspace_file_create(wid, content=content)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
content = '/path/to/file' # file | File contents in binary. (optional)

try:
    # Upload file.
    api_response = api_instance.workspace_file_create(wid, content=content)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_file_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **content** | **file**| File contents in binary. | [optional] 

### Return type

[**BaseMetadata**](BaseMetadata.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_details**
> MetadataByFamily workspace_file_details(wid, uuid)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier

try:
    # Fetch file.
    api_response = api_instance.workspace_file_details(wid, uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_file_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 

### Return type

[**MetadataByFamily**](MetadataByFamily.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/octet-stream, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_fetch**
> PaginatedFiles workspace_file_fetch(wid, page=page, per_page=per_page, filters=filters)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)
filters = filename=foo.png,path=images,size=12314 # str | Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. (optional)

try:
    # List files.
    api_response = api_instance.workspace_file_fetch(wid, page=page, per_page=per_page, filters=filters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_file_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]
 **filters** | **str**| Filters on the workspace files, separated by commas. These filters are applied only the base metadata family. This can be used to get a file by name, path, size or checksum. | [optional] 

### Return type

[**PaginatedFiles**](PaginatedFiles.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_set_metadata**
> MetadataByFamily workspace_file_set_metadata(wid, uuid, metadata_by_family=metadata_by_family)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier
metadata_by_family = quetzal._auto_client.MetadataByFamily() # MetadataByFamily |  (optional)

try:
    # Rewrite metadata.
    api_response = api_instance.workspace_file_set_metadata(wid, uuid, metadata_by_family=metadata_by_family)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_file_set_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 
 **metadata_by_family** | [**MetadataByFamily**](MetadataByFamily.md)|  | [optional] 

### Return type

[**MetadataByFamily**](MetadataByFamily.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_file_update_metadata**
> MetadataByFamily workspace_file_update_metadata(wid, uuid, metadata_by_family=metadata_by_family)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
uuid = 'uuid_example' # str | File identifier
metadata_by_family = quetzal._auto_client.MetadataByFamily() # MetadataByFamily |  (optional)

try:
    # Modify metadata.
    api_response = api_instance.workspace_file_update_metadata(wid, uuid, metadata_by_family=metadata_by_family)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_file_update_metadata: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **uuid** | [**str**](.md)| File identifier | 
 **metadata_by_family** | [**MetadataByFamily**](MetadataByFamily.md)|  | [optional] 

### Return type

[**MetadataByFamily**](MetadataByFamily.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_create**
> Query workspace_query_create(wid, query, page=page, per_page=per_page)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
query = quetzal._auto_client.Query() # Query | 
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # Prepare a query.
    api_response = api_instance.workspace_query_create(wid, query, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_query_create: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **query** | [**Query**](Query.md)|  | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**Query**](Query.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_details**
> Query workspace_query_details(wid, qid, page=page, per_page=per_page)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
qid = 56 # int | Query identifier
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # Query details.
    api_response = api_instance.workspace_query_details(wid, qid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_query_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **qid** | **int**| Query identifier | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**Query**](Query.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_query_fetch**
> PaginatedQueries workspace_query_fetch(wid, page=page, per_page=per_page)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.
page = 1 # int | The page of a collection to return. (optional) (default to 1)
per_page = 100 # int | Number of items to return per page. (optional) (default to 100)

try:
    # List queries.
    api_response = api_instance.workspace_query_fetch(wid, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_query_fetch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 
 **page** | **int**| The page of a collection to return. | [optional] [default to 1]
 **per_page** | **int**| Number of items to return per page. | [optional] [default to 100]

### Return type

[**PaginatedQueries**](PaginatedQueries.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_scan**
> Workspace workspace_scan(wid)

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
api_instance = quetzal._auto_client.DataApi(quetzal._auto_client.ApiClient(configuration))
wid = 56 # int | Workspace identifier.

try:
    # Update views.
    api_response = api_instance.workspace_scan(wid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->workspace_scan: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **wid** | **int**| Workspace identifier. | 

### Return type

[**Workspace**](Workspace.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/problem+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

