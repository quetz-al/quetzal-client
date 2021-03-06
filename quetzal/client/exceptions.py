import json
import textwrap
import warnings

from requests import codes


class QuetzalAPIException(Exception):
    """ Exception for errors sent by the Quetzal API.

    Errors in Quetzal API are responses that follow
    `RFC-7807 <https://tools.ietf.org/html/rfc7807>`_. This exception object
    is generated from these responses.

    Attributes
    ----------
    status: int
        HTTP error code.
    title: str
        Title of the problem.
    detail:
        Human-readable detailed message on the problem.


    """

    def __init__(self, status, title, detail):
        self.status = status or 'Unknown status code'
        self.title = title or 'No title provided'
        self.detail = detail or 'No details provided'
        super().__init__(f'{self.title} (status={self.status})')

    def __reduce__(self):  # Needed for pickleable exceptions
        return type(self), (self.status, self.title, self.detail)

    @staticmethod
    def from_api_exception(api_exception, authorize_ok=False):
        """ Generate a QuetzalAPIException from the auto-generated exception type.

        Parameters
        ----------
        api_exception: quetzal.openapi_client.rest.ApiException
            The exception generated by the auto-generated code
        authorize_ok: bool, optional
            When ``True``, raise a :py:class:`RetryableException` when the status
            code is 401 so that the caller may retry after a login.

        Returns
        -------
        quetzal.client.QuetzalAPIException

        """

        status = api_exception.status
        title = 'unknown'
        detail = 'A problem occurred, but the API did not generate a JSON error response.'
        try:
            body = json.loads(api_exception.body)
            status = body.get('status', status)
            title = body.get('title', 'unknown')
            detail = body.get('detail', 'A problem occurred, but the API did not '
                                        'generate a standard error response.')
        except (json.JSONDecodeError, TypeError):
            pass

        if status == codes.unauthorized:
            if authorize_ok:
                cls = RetryableException
            else:
                cls = UnauthorizedException
        elif status in (codes.bad_request, codes.forbidden, codes.not_found,
                        codes.precondition_failed, codes.server_error):
            cls = QuetzalAPIException
        else:
            cls = RetryableException
        return cls(status, title, detail)

    def __str__(self):
        error_message = f"""
        Quetzal API responded with a problem:
            status: {self.status}
            title: {self.title}
            details: {self.detail}
        """
        return textwrap.dedent(error_message).strip()


class RetryableException(QuetzalAPIException):
    """A Quetzal API exception to an operation that may be retried."""
    pass


# class NonRetryableException(QuetzalAPIException):
#     pass


class UnauthorizedException(QuetzalAPIException):
    """A Quetzal API exception specific for unauthorized access."""
    pass
