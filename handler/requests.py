import requests
from django.conf import settings


# Wrapper for debug token insertion

def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }
    return requests.request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }
    return requests.request("options", url, **kwargs)


def head(url, **kwargs):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes. If
        `allow_redirects` is not provided, it will be set to `False` (as
        opposed to the default :meth:`request` behavior).
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }

    kwargs.setdefault("allow_redirects", False)
    return requests.request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    r"""Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }

    return requests.request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    r"""Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }

    return requests.request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    if settings.DEBUG_TOKEN != "":
        if "headers" in kwargs:
            kwargs["headers"]["X-Debug-Token"] = settings.DEBUG_TOKEN
        else:
            kwargs["headers"] = {
                "X-Debug-Token": settings.DEBUG_TOKEN
            }

    return requests.request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return requests.request("delete", url, **kwargs)
