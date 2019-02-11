# Workspace

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Workspace ID | [optional] 
**status** | **str** | Workspace status | [optional] 
**creation_date** | **datetime** | Date when the workspace was created | [optional] 
**owner** | **str** | User who owns this workpace | [optional] 
**data_url** | **str** | URL of a remote storage location for files used in this workspace | [optional] 
**name** | **str** | Name of the workspace | 
**description** | **str** | Descriptive text of the purpose of this workspace | 
**families** | [**object**](.md) | Families and corresponding versions used in this workspace. This property is a object whose keys are family names and values are integers. | 
**temporary** | **bool** | Whether this workspace is temporary or not. Temporary workspaces are automatically deleted after some time. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


