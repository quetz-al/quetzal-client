import backoff


def create(client, name, description, families, temporary=False, wait=False, progress=None):
    """ Create a workspace.

    This function calls the Quetzal API endpoint to create a workspace.
    When the `wait` option is set, this function will continously call the
    workspace detail endpoint until the workspace status is no longer
    *INITIALIZING*.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    name: str
        Name for the new workspace.
    description: str
        Description for the new workspace.
    families: dict
        Family and versions for the new workspace. In this dictionary, keys
        are interpreted as family names, values as versions.
    temporary: bool, optional
        Temporary boolean flag set when creating the workspace. By default,
        ``False``.
    wait: bool, optional
        When ``False``, this function returns after the POST request. When
        ``True``, it will request the details of the workspace until it has
        finished its initialization.
    progress: dict, optional
        Progress function and parameters. See :py:func:`wait_for_workspace`.

    Returns
    -------
    w_details: quetzal.openapi_client.models.Workspace
        Details on the created workspace.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """

    workspace_create_object = {
        "name": name,
        "description": description,
        "families": families,
        'temporary': temporary,
    }
    w_details = client.workspace_create(workspace_create_object)

    if wait:
        w_details = wait_for_workspace(client,
                                       w_details.id,
                                       lambda w: w.status == 'INITIALIZING',
                                       progress)
    return w_details


def list_(client, name=None, owner=None, deleted=False, per_page=100, limit=1000):
    """ List existing workpaces.

    This function calls the Quetzal API endpoint to list workspaces and manages
    the paginated response to retrieve as many results as set by the `limit`
    parameter.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    name: str, optional
        Filter workspaces by this name.
    owner: str, optional
        Filter workspaces by this username.
    deleted: bool, optional
        When ``True``, include *DELETED* workspaces.
    per_page: int, optional
        Number of items to request per page.
    limit: int, optional
        Limit the number of workspaces to fetch.

    Returns
    -------
    results: list
        A list of workspace details as dictionaries.
    total: int
        The total number of workspaces that exist. Note that this may be
        higher than the number of objects returned.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """
    kwargs = dict(per_page=min(per_page, limit), page=1)
    if name:
        kwargs['name'] = name
    if owner:
        kwargs['owner'] = owner
    if deleted:
        kwargs['deleted'] = True

    page = client.workspace_fetch(**kwargs)

    results = [w.to_dict() for w in page.results]  # TODO: reconsider this to_dict here!
    while len(results) < limit and len(results) < page.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        page = client.workspace_fetch(**kwargs)
        results.extend([w.to_dict() for w in page.results])

    return results, page.total


def details(client, wid=None, name=None, owner=None):
    """ Fetch the details of a workspace by name or id.

    This function calls the Quetzal API endpoint to retrieve workspace
    details. When the `wid` parameter is set, it will use directly this number
    to do a `GET` on `/workspaces/:id`. When the `name` is set, it will fetch
    and filter the workspace list by this name and its `owner`. Note that
    `name` and `wid` are mutually exclusive options.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int, optional
        Workspace identifier.
    name: str, optional
        Workspace name.
    owner: str, optional
        Username of the workspace owner. If not set and `name` is set, it will
        use the username saved on the `client` configuration object.

    Returns
    -------
    w_details: quetzal.openapi_client.models.Workspace
        Details on the workspace, or ``None`` when it was not found.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error. When the `wid` parameter is set and the
        workspace does not exist, this exception will be raised with its
        `status` member set to 404 (not found).
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """
    if wid is None and name is None:
        raise ValueError('One of wid or name is needed.')

    if name:
        username = owner or client.configuration.username
        response = client.workspace_fetch(owner=username, name=name)
        if not response.results:
            return None
        w_details = response.results[0]
    else:
        w_details = client.workspace_details(wid)
    return w_details


def commit(client, wid, wait=False, progress=None):
    """ Commit a workspace.

    This function calls the Quetzal API endpoint to commit a workspace. When
    the `wait` option is set, this function will continously call the
    workspace detail endpoint until the workspace status is no longer
    *COMMITTING*.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int
        Workspace identifier.
    wait: bool, optional
        When ``False``, this function returns after the PUT request. When
        ``True``, it will request the details of the workspace until the commit
        operation finishes.
    progress: dict, optional
        Progress function and parameters. See :py:func:`wait_for_workspace`.

    Returns
    -------
    w_details: quetzal.openapi_client.models.Workspace
        Details on the workspace after committing.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """

    w_details = client.workspace_commit(wid)

    if wait:
        w_details = wait_for_workspace(client,
                                       w_details.id,
                                       lambda w: w.status == 'COMMITTING',
                                       progress)
    return w_details


def scan(client, wid, wait=False, progress=None):
    """ Scan a workspace, preparing the views for querying it.

    This function calls the Quetzal API endpoint to scan a workspace. When
    the `wait` option is set, this function will continously call the
    workspace detail endpoint until the workspace status is no longer
    *SCANNING*.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int
        Workspace identifier.
    wait: bool, optional
        When ``False``, this function returns after the PUT request. When
        ``True``, it will request the details of the workspace until the commit
        operation finishes.
    progress: dict, optional
        Progress function and parameters. See :py:func:`wait_for_workspace`.

    Returns
    -------
    w_details: quetzal.openapi_client.models.Workspace
        Details on the workspace after scanning.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """

    w_details = client.workspace_scan(wid)

    if wait:
        w_details = wait_for_workspace(client,
                                       w_details.id,
                                       lambda w: w.status == 'SCANNING',
                                       progress)
    return w_details


def files(client, wid, per_page=100, limit=1000, **filters):
    """ List files uploaded or whose metadata has changed on a workspace.

    This function calls the Quetzal API endpoint to list workspace files and
    manages the paginated response to retrieve as many results as set by the
    `limit` parameter.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int
        Workspace identifier.
    per_page: int, optional
        Number of items to request per page.
    limit: int, optional
        Limit the number of workspaces to fetch.
    **filters
        Filters on the base metadata of the file. For example,
        `filename='foo.bin', size=1024`

    Returns
    -------
    results: list
        A list of file details objects.
    total: int
        The total number of files that exist in the workspace. Note that this
        may be higher than the number of objects returned.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """
    kwargs = dict(per_page=min(per_page, limit), page=1)
    filter_strings = []
    for k, v in filters.items():
        filter_strings.append(f'{k}={v}')
    if filter_strings:
        kwargs['filters'] = ','.join(filter_strings)
    page = client.workspace_file_fetch(wid, **kwargs)
    file_list = [r.to_dict() for r in page.results]
    while len(file_list) < limit and len(file_list) < page.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        fetch_result = client.workspace_file_fetch(wid, **kwargs)
        file_list.extend([r.to_dict() for r in fetch_result.results])

    return file_list, page.total


def upload(client, wid, file, **kwargs):
    """ Upload a file to a workspace.

    This function calls the Quetzal API endpoint to upload a file into a
    workspace.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int
        Workspace identifier.
    file: file-like object
        A file object, like the returned objects of ``io.Open``. It must have a
        name attribute (used to set the filename metadata) and a read method.

    Returns
    -------
    file_details: quetzal.openapi_client.models.BaseMetadata
        Uploaded file details.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """
    if not hasattr(file, 'read') or not hasattr(file, 'name'):
        raise ValueError('file must have a read method and name attribute.')
    file_details = client.workspace_file_create(wid, content=file.name, **kwargs)
    return file_details


def update_metadata(client, wid, file_id, metadata):
    # from quetzal.openapi_client.models.metadata_by_family import MetadataByFamily
    # obj = MetadataByFamily(id=file_id, metadata=metadata)
    obj = {
        'metadata': metadata
    }
    response = client.workspace_file_update_metadata(wid=wid, uuid=file_id,
                                                     metadata_by_family=obj)
    return response


def wait_for_workspace(client, wid, retry_predicate, progress=None):
    """ Wait until a workspace satisfies a condition.

    This function *continously* calls the Quetzal API endpoint to retrieve
    workspace details until the `retry_predicate` function returns a value that
    evaluates to ``False``. When the predicate gives a ``True`` result, this
    function will wait 1 second and then try again.

    The `progress` parameter of this function is designed for showing
    progression messages while this function waits. It should be either
    ``None`` for no progress messages or a dictionary that has four keys:

    * **func**: a callable or function that will be evaluated after
      each call to workspace details. It should accept a positional
      argument that will have the workspace details and then the extra
      arguments and keywork arguments described next.

    * **clear**: a callable or function that will be evaluated at the end
      of the wait (when the predicate evaluates to ``True``). It should
      have the same signature as `func`.

    * **args**: Extra arguments passed to `func` and `clear`.

    * **kwargs**: Extra keyword-arguments passed to `func` and `clear`.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used for the Quetzal API operation.
    wid: int
        Workspace identifier.
    retry_predicate: callable
        A function or callable that will be evaluated every second. It
        must handle exacly one positional parameter. This parameter will
        be a workspace detail object.
    progress: dict, optional
        A dictionary with the configuration for progress function callbacks.

    Returns
    -------
    w_details: quetzal.openapi_client.models.Workspace
        Details on the workspace; the result of the latest workspace detail
        call.

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.
    urllib3.exceptions.RequestError
        When there was a problem connecting to the server.

    """

    if progress is not None:
        progress_func = progress.get('func', None)
        progress_clear = progress.get('clear', None)
        progress_args = progress.get('args', ())
        progress_kwargs = progress.get('kwargs', {})
    else:
        progress_func = _noop
        progress_clear = _noop
        progress_args = ()
        progress_kwargs = {}

    @backoff.on_predicate(backoff.constant, retry_predicate, interval=1)
    def poll():
        w_details = client.workspace_details(wid)
        if progress_func:
            args = (w_details,) + progress_args
            progress_func(*args, **progress_kwargs)
        return w_details

    result = poll()
    args = (result,) + progress_args
    progress_clear(*args, **progress_kwargs)
    return result


def delete(client, wid, wait=False, progress=None):

    client.workspace_delete(wid)
    if wait:
        w_details = wait_for_workspace(client,
                                       wid,
                                       lambda w: w.status == 'DELETING',
                                       progress)
        return w_details
    else:
        return None


def _noop(*args, **kwargs):
    # No operation. Receive args and kwargs and return None
    pass

