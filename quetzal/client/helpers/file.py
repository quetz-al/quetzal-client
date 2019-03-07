import functools
import logging
import pathlib

from quetzal.client.utils import get_data_dir, get_readable_info


logger = logging.getLogger(__name__)


def download(client, file_id=None, wid=None, *, output=None, output_dir=None, **kwargs):

    if output is None and output_dir is None:
        raise ValueError('Missing output or output_dir keyword argument.')

    if file_id is None:
        file_details = _find_file(client, wid, **kwargs)
        if file_details is None:
            raise ValueError('File not found')
        file_id = file_details.id
    elif kwargs:
        raise ValueError('Use id or kwargs filters, but not both.')

    # Default to the user's data directory
    output_dir = output_dir or get_data_dir()
    output_dir = pathlib.Path(output_dir)

    file_metadata = metadata(client, file_id, wid)
    base = file_metadata['base']
    if output_dir is not None:
        output = output_dir / base['path'] / base['filename']
    else:
        output = pathlib.Path(output)

    # Before downloading, check if the file already exists and has the correct
    # size and checksum
    if output.exists():
        with output.open('rb') as f:
            md5, size = get_readable_info(f)
        if md5 == base['checksum'] and size == base['size']:
            logger.debug('File %s already downloaded in %s', file_id, output)
            return str(output.resolve())

    # The file does not exist locally, let's download it
    # Use the file details in workspace or outside workspace function
    if wid is None:
        func = functools.partial(client.public_file_details, uuid=file_id)
    else:
        func = functools.partial(client.workspace_file_details, wid=wid, uuid=file_id)

    contents = func(_accept='application/octet-stream', _preload_content=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        f.write(contents.data)

    return str(output.resolve())


def metadata(client, file_id, wid=None):
    # Use the file details in workspace or outside workspace function
    if wid is None:
        func = functools.partial(client.public_file_details, uuid=file_id)
    else:
        func = functools.partial(client.workspace_file_details, wid=wid, uuid=file_id)

    metadata_response = func(_accept='application/json')
    return metadata_response['metadata']


def _find_file(client, wid=None, **kwargs):
    filters = ','.join([f'{k}={v}' for k, v in kwargs.items()])
    if wid is None:
        func = functools.partial(client.public_file_fetch)
    else:
        func = functools.partial(client.workspace_file_fetch, wid=wid)

    fetch_result = func(filters=filters)
    if fetch_result.total == 0:
        return None
    elif fetch_result.total > 1:
        raise ValueError(f'Several files match filter {filters}.')
    return fetch_result.results[0]
