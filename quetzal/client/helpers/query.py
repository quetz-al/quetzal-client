import functools
import sys


def query(client, wid, query_contents, dialect='postgresql', limit=None):
    """Query metadata."""

    if limit is None:
        kwargs = dict(per_page=100)
        limit = sys.maxsize
    else:
        kwargs = dict(per_page=min(limit, 100))

    query_obj = {
        'dialect': dialect,
        'query': query_contents,
    }

    if wid is None:
        query_details = client.public_query_create(query_obj, **kwargs)
        details_func = client.public_query_details
    else:
        query_details = client.workspace_query_create(wid, query_obj, **kwargs)
        details_func = functools.partial(client.workspace_query_details, wid)

    results = query_details.results
    if not results:
        return [], 0

    # The query POST action redirects to the GET details but does not have
    # a per_page, so we might get more that we needed
    if len(results) > limit:
        results = results[:limit]

    while len(results) < limit and len(results) < query_details.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        query_details = details_func(query_details.id, **kwargs)
        results.extend(query_details.results)

    return results, query_details.total
