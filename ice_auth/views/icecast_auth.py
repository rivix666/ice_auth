from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import insert

from datetime import datetime
from parse import parse

from ice_auth import models
from ice_auth.utils import logs

class ListenerAuthView:
    def __init__(self, request):
        self.request = request

    # Method used to authenticate new listeners, that are trying to connect with icecast
    #---------------------------------------------------------------------------------------------------
    @view_config(route_name = 'icecast_listener_add', request_method = 'POST')
    def listener_add(self):
        log = logs.ice_log(__name__, self.request)

        # Try to find listener by the data from POST
        listener = self.findListenerByPost()
        if not listener:
            raise exc.HTTPUnauthorized()

        # If there is no access data connected to current listener, raise exception
        access = self.accessParams(listener)
        if not access:
            log.critical('There is no access data for listener with id {}'
                        .format(listener.id, True))
            raise exc.HTTPInternalServerError()

        # Check if user has active account
        if datetime.now().date() > access.expiration_date:
            raise exc.HTTPForbidden()

        # Check if user is not already connected
        if self.countActiveListeners(listener) >= access.max_listeners:
            raise exc.HTTPForbidden()

        # Add user to active_listeners table
        new_listener = models.ActiveListeners(listener_id = listener.id, listener_ip = self.request.remote_addr)
        self.request.dbsession.add(new_listener)

        log.info('Listener with id {} connected to icecast'.format(listener.id))
        return Response(headerlist=[("listener_accepted", "1")], status_int = 200)

    # Method used to remove disconnecting listeners from active listeners table
    #---------------------------------------------------------------------------------------------------
    @view_config(route_name = 'icecast_listener_remove', request_method = 'POST')
    def listener_remove(self):
        log = logs.ice_log(__name__, self.request)

        # Try to find listener by the data from POST
        listener = self.findListenerByPost()
        if not listener:
            raise exc.HTTPUnauthorized()

        if self.countActiveListeners(listener) <= 0:
            log.critical('Number of active listeners is <= 0 during listener_remove. | Listener id: {}'.format(listener.id), True)
            raise exc.HTTPInternalServerError()

        # Try to find active listener with given id and ip
        query = self.request.dbsession.query(models.ActiveListeners)
        listener_to_remove = query.filter(models.ActiveListeners.listener_id == listener.id).filter(models.ActiveListeners.listener_ip == self.request.remote_addr).first()

        # If there is no active listener that match to given ip, remove first with given id
        if not listener_to_remove:
            listener_to_remove = query.filter(models.ActiveListeners.listener_id == listener.id).first()

        # Check if we finally find him
        if not listener_to_remove:
            log.critical('Can not find listener with given id during listener_remove. | Listener id: {}'.format(listener.id), True)
            raise exc.HTTPInternalServerError()

        self.request.dbsession.delete(listener_to_remove)   
        log.info('Listener with id {} disconnected from icecast'.format(listener.id))  
        return Response(status_int = 200)

    #---------------------------------------------------------------------------------------------------
    def findListenerByPost(self):
        # Get uuid from POST sent by icecast
        listener_uuid = self.uuidFromPost()

        # Try to find listener with given uuid
        listener = self.findListener(listener_uuid)
        if not listener:
            raise exc.HTTPUnauthorized()

        return listener

    #---------------------------------------------------------------------------------------------------
    def uuidFromPost(self):   
        # Try to get mount data from POST
        icecast_data = self.request.params['mount']
        
        # Parse 'mount' data to get uuid (eg. data: '/auth_test?uuid=222-222')
        parsed_data = parse('/{}?uuid={}', icecast_data)
        if not parsed_data:
            log = logs.ice_log(__name__, self.request)
            log.error('Can not parse uuid', True)
            raise exc.HTTPBadRequest()

        # Try to get uuid from parsed data
        listener_uuid = parsed_data[-1]
        return listener_uuid

    #---------------------------------------------------------------------------------------------------
    def findListener(self, listener_uuid):
        query = self.request.dbsession.query(models.Listeners)
        listener = query.filter(models.Listeners.uuid == listener_uuid).first()
        return listener

    #---------------------------------------------------------------------------------------------------
    def accessParams(self, listener):
        log = logs.ice_log(__name__, self.request)
        if len(listener.access) != 1:
            log.critical('The number of access data for listener with id {} is different than 1. | Access data num: {}'
                        .format(len(listener.access)), True)
            raise exc.HTTPInternalServerError()
        return listener.access[0]

    #---------------------------------------------------------------------------------------------------
    def countActiveListeners(self, listener):
        return len(listener.active_listeners)
