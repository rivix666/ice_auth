from pyramid.response import Response
from pyramid.view import exception_view_config
import pyramid.httpexceptions as http_exc
from sentry_sdk import capture_exception
from ice_auth.utils import logs

@exception_view_config(Exception)
def exception_view(exc, request):
    log = logs.ice_log(__name__, request)
    log.warn('[EXCEPTION] [NAME {}] {}'.format(type(exc).__name__, exc))
    capture_exception(exc)
    return Response(status_int = 500)

@exception_view_config(http_exc.HTTPException)
def http_exception_view(exc, request):
    log = logs.ice_log(__name__, request)
    log.info('[HTTP_EXCEPTION] [NAME {}] [CODE {}]'.format(type(exc).__name__, exc.code))
    return Response(status_int = exc.code)