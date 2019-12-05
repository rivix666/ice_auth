from pyramid.response import Response
from pyramid.view import exception_view_config
import pyramid.httpexceptions as exceptions
from sentry_sdk import capture_exception
from main.utils import logs

@exception_view_config(Exception)
def exception_view(exc, request):
    if isinstance(exc, Exception):
        log = logs.ice_log(__name__, request)
        log.warn('[EXCEPTION][NAME {}] {}'.format(type(exc).__name__, exc))
        if isinstance(exc, exceptions.HTTPException):
            return Response(status_int = exc.code)
        else:
            capture_exception(exc)

    return Response(status_int = 500)