from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import insert

from datetime import datetime
from parse import parse

from .. import models

# TODO! Add loggs

class ListenerAuthView:
    def __init__(self, request):
        self.request = request

    #################################################################################################
    @view_config(route_name = 'not_found_404')
    def not_found_404(self):
        response = render_to_response('../templates/404.jinja2', '', request = self.request)
        response.content_type = 'text/html'
        response.status_int = 404
        return response

    # Method used to authenticate new listeners, that are trying to connect with icecast
    @view_config(route_name = 'icecast_listener_add', request_method = 'POST')
    def listener_add(self):
        # Get uuid from POST sent by icecast
        listener_uuid = self.uuidFromPost()
        if not listener_uuid:
            return HTTPFound(location = '/')
        
        # Try to find listener with given uuid
        listener = self.findListener(listener_uuid)
        if not listener:
            return HTTPFound(location = '/')

        # If there is no access data connected to current listener, then go to 404
        access = listener.accessParams()
        if not access:
            print(3)
            return HTTPFound(location = '/')

        # Check if user has active account
        if datetime.now().date() > access.expiration_date:
            print(4)
            return HTTPFound(location = '/')

        # Check if user is not already connected
        if listener.countActiveListeners() >= access.max_listeners:
            print(5)
            return HTTPFound(location = '/')

        # Add user to active_listeners table
        try:
            new_listener = models.ActiveListeners(listener_id = listener.id, listener_ip = self.request.remote_addr)
            self.request.dbsession.add(new_listener)
            self.request.dbsession.flush()
        except DBAPIError:
            print(6)
            return HTTPFound(location = '/')

        return Response(headerlist=[("listener_accepted", "1")], status_int = 200)

    # Method used to remove disconnecting listeners from active listeners table
    @view_config(route_name = 'icecast_listener_remove', request_method = 'POST')
    def listener_remove(self):
        # Get uuid from POST sent by icecast
        listener_uuid = self.uuidFromPost()
        if not listener_uuid:
            return HTTPFound(location = '/')
        
        # Try to find listener with given uuid
        listener = self.findListener(listener_uuid)
        if not listener:
            return HTTPFound(location = '/')

        if listener.countActiveListeners() <= 0:
            # TODO LOGS!!!!
            return Response(status_int = 501)

        # TODO
        try:
            query = self.request.dbsession.query(models.ActiveListeners)
            listener_to_remove = query.filter(models.ActiveListeners.listener_id == listener.id).first()

            # TODO wogole pomyslec co wtedy jak takiego ip nie bedzie na liscie, zalogować to i olać?
            # czy w ogóle mi jest potrzebne ip? przydaloby sie do obczajania jaki suer z jakich ip slucha
            # moze dorobic tabele ktora by trzymala ip wykorzystywane przez usera i ew z tamtad je wywalac a jak nie bedzie
            # takiego ip tam to trudno
            #listener_to_remove = query.filter(models.ActiveListeners.listener_ip == self.request.remote_addr).first()
            
        except DBAPIError:
            print(1)
            return Response(status_int = 502)

        if not listener_to_remove:
            return Response(status_int = 503)

        self.request.dbsession.delete(listener_to_remove)
        self.request.dbsession.flush()
        
        return Response(status_int = 200)

    #################################################################################################
    def uuidFromPost(self):         
        # Try to get mount data from POST
        try:
            icecast_data = self.request.params['mount']
        except KeyError:
            print(-2)
            return None
        
        # Parse 'mount' data to get uuid (eg. data: '/auth_test?uuid=222-222')
        parsed_data = parse('/{}?uuid={}', icecast_data)
        if not parsed_data:
            print(-1)
            return None

        # Try to get uuid from parsed data
        try:    
            listener_uuid = parsed_data[-1]
        except IndexError:
            print(0)
            return None

        return listener_uuid

    def findListener(self, listener_uuid):
        try:
            query = self.request.dbsession.query(models.Listeners)
            listener = query.filter(models.Listeners.uuid == listener_uuid).first()
        except DBAPIError:
            print(1)
            return None
        return listener
        
