from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import insert

from datetime import datetime

from ice_auth import models
from ice_auth.utils import logs

class ListenerMgr:
    def __init__(self, request):
        self.request = request

    # Add new listener into database
    #---------------------------------------------------------------------------------------------------
    @view_config(route_name = 'icecast_listener_register', request_method = 'POST')
    def listener_new(self):
        log = logs.ice_log(__name__, self.request)

        #TODO add maybe some sort of authentication between wordpress and this

        # Try to get listener data from POST
        try:
            new_user_uuid = self.request.params['uuid']
            new_user_exp_date = self.request.params['exp_date']
            new_user_licences_num = self.request.params['licences_num']
        except KeyError as e:
            log.critical('Wrong POST {}'.format(e))
            raise e

        # Check if there is no already registered listener with given uuid
        query = self.request.dbsession.query(models.Listeners)
        listener = query.filter(models.Listeners.uuid == new_user_uuid).first()
        if listener:
            # log.critical('Someone tries to register listener that already exists (id {}) (uuid {})'.format(listener.id, listener.uuid), True)
            return Response(status_int = 234) # 234 means that user was skipped 

        # Add new listener  
        new_listener = models.Listeners(uuid = new_user_uuid)
        self.request.dbsession.add(new_listener)
        self.request.dbsession.flush() # this flush needs to be here, cause we want to use auto incremented id as listener_id below

        new_listener_access = models.IcecastAccess(listener_id = new_listener.id
                                                    , max_listeners = new_user_licences_num
                                                    , expiration_date = datetime.strptime(new_user_exp_date, '%Y-%m-%d'))
        self.request.dbsession.add(new_listener_access)

        log.info('Listener with id {} registered'.format(new_listener.id)) 
        return Response(status_int = 200)

    # Remove listener from database
    #---------------------------------------------------------------------------------------------------
    @view_config(route_name = 'icecast_listener_unregister', request_method = 'POST')
    def listener_delete(self):
        log = logs.ice_log(__name__, self.request)

        #TODO add maybe some sort of authentication between wordpress and this

        # Try to get listener data from POST
        try:
            new_user_uuid = self.request.params['uuid']
        except KeyError as e:
            log.critical('Wrong POST {}'.format(e))
            raise e

        # Check if listener with given uuid exists
        query = self.request.dbsession.query(models.Listeners)
        listener = query.filter(models.Listeners.uuid == new_user_uuid).first()
        if not listener:
            log.critical('Someone tries to unregister listener that not exists (uuid {})'.format(new_user_uuid), True)
            raise exc.HTTPInternalServerError()

        # Delete listener 
        listener_id = listener.id
        self.request.dbsession.delete(listener)   
        log.info('Listener with id {} unregistered'.format(listener_id)) 
        return Response(status_int = 200)
