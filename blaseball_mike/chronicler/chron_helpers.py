from blaseball_mike.session import check_network_response


def prepare_id(id_):
    """
    if id_ is string uuid, return as is, if list, format as comma separated list.
    """
    if isinstance(id_, list):
        return ','.join(id_)
    elif isinstance(id_, str):
        return id_
    else:
        raise ValueError(f'Incorrect ID type: {type(id_)}')


def paged_get(url, params, session, total_count=None, page_size=250, lazy=False):
    """
    Combine paged URL responses
    """
    if lazy:
        return paged_get_lazy(url, params, session, total_count, page_size)

    if total_count is not None and total_count < page_size:
        page_size = total_count

    params["count"] = page_size
    data = []
    while True:
        out = check_network_response(session.get(url, params=params))
        if "items" in out:
            d = out["items"]
        else:
            d = out.get("data", [])
        page = out.get("nextPage")

        data.extend(d)
        if page is None or len(d) == 0 or len(d) < page_size:
            break

        if total_count is not None:
            total_count -= len(d)
            if total_count <= 0:
                break
            if total_count < page_size:
                page_size = total_count
                params["count"] = page_size

        params["page"] = page

    return data


def paged_get_lazy(url, params, session, total_count=None, page_size=250):
    """
    Combine paged URL responses; returns a generator
    """
    if total_count is not None and total_count < page_size:
        page_size = total_count

    params["count"] = page_size
    while True:
        out = check_network_response(session.get(url, params=params))
        if "items" in out:
            d = out["items"]
        else:
            d = out.get("data", [])
        page = out.get("nextPage")

        yield from d
        if page is None or len(d) == 0 or len(d) < page_size:
            break

        if total_count is not None:
            total_count -= len(d)
            if total_count <= 0:
                break
            if total_count < page_size:
                page_size = total_count
                params["count"] = page_size

        params["page"] = page
