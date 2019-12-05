import sentry_sdk
from sentry_sdk.integrations.pyramid import PyramidIntegration

from pyramid.config import Configurator

def main(global_config, **settings):
    """ Comment
    """
    sentry_sdk.init(
        dsn="https://9fe237b050b645349c72dda7adbd10f5@sentry.io/1845128",
        integrations=[PyramidIntegration()]
    )

    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
