# from pyramid.view import view_config, view_defaults
# from pyramid.response import Response
# from .. import models

# @view_defaults(route_name='home', renderer='../templates/mytemplate.jinja2')


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     return  return {'one': 'lkkkk', 'project': 'ice_auth'}
#     # try:
#     #     query = request.dbsession.query(models.MyModel)
#     #     one = query.filter(models.MyModel.name == 'one').first()
#     # except DBAPIError:
#     #     return Response(db_err_msg, content_type='text/plain', status=500)
#     # return {'one': one, 'project': 'ice_auth'}
