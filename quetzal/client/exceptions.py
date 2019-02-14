import json
import textwrap
import warnings

from requests import codes


class QuetzalAPIException(Exception):

    def __init__(self, status, title, detail):
        super().__init__(f'{title} (status={status})')
        self.status = status
        self.title = title
        self.detail = detail

    @staticmethod
    def from_api_exception(api_exception, authorize_ok=False):
        if not hasattr(api_exception, 'body') or not api_exception.body:
            if api_exception.status == codes.precondition_failed:
                warnings.warn('Due to werkzeug issue #1231, we will not receive'
                              ' the problem details when a code 412 occurs',
                              RuntimeWarning, stacklevel=2)
            return QuetzalAPIException(api_exception.status,
                                       api_exception.reason,
                                       'No details available')
        try:
            body = json.loads(api_exception.body)
            status = body.get('status', -1)
            title = body.get('title', 'unknown')
            detail = body.get('detail', '')

        except (json.JSONDecodeError, TypeError):
            return QuetzalAPIException(-1, 'unknown', '')

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
        """Custom error messages for exception"""
        error_message = f"""
        Quetzal API responded with a problem:
            status: {self.status}
            title: {self.title}
            details: {self.detail}
        """
        return textwrap.dedent(error_message).strip()


class RetryableException(QuetzalAPIException):
    pass


# class NonRetryableException(QuetzalAPIException):
#     pass


class UnauthorizedException(QuetzalAPIException):
    pass
