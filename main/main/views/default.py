from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {'one': 'lkkkk', 'project': 'ice_auth'}
    # try:
    #     query = request.dbsession.query(models.MyModel)
    #     one = query.filter(models.MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    # return {'one': one, 'project': 'ice_auth'}

@view_config(route_name="icecast_listener_add")
def kaka(request):
    #headers = [('icecast-auth-user')]
    #return Response(headerlist=headers, status_int=1)

    headers = [("icecast-auth-user", "1")]
    return Response(headerlist=headers, status_int=200)