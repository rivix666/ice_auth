from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import insert

from datetime import datetime
from parse import parse

from .. import models

import socket

from sentry_sdk import capture_exception
from sentry_sdk import capture_message

import logging

# TODO! Add loggs


class ListenerMgr:
    def __init__(self, request):
        self.request = request

    # Add ne listeners into database ()
    @view_config(route_name = 'icecast_listener_new', request_method = 'POST')
    def listener_add(self):
        log = logging.getLogger(__name__)
        log.debug('test log')

        capture_message("test")

        # Try to get mount data from POST
        try:
            new_user_uuid = self.request.params['uuid']
            new_user_exp_date = self.request.params['exp_date']
            new_user_licences_num = self.request.params['licences_num']
        except KeyError:
            print("O MAMUSIU!!")
            capture_exception()
            return Response(status_int = 500) #zamienic na jakis kod bledu, dodac log

        # ssprawdzamy czy listenera czasem nie ma już w bazie
        try:
            query = self.request.dbsession.query(models.Listeners)
            listener = query.filter(models.Listeners.uuid == new_user_uuid).first()
        except DBAPIError:
            print('KEKE')
            return HTTPFound(location = '/') #zamienic na jakis kod bledu, dodac log
        
        if listener:
            print("hołhołhoł")
            return HTTPFound(location = '/') #zamienic na jakis kod bledu, dodac log

        # dodajemy listenera
        try:
            new_listener = models.Listeners(uuid = new_user_uuid)
            self.request.dbsession.add(new_listener)
            self.request.dbsession.flush() # this flush needs to be here, cause we want to use auto incremented id as listener_id below

            new_listener_access = models.IcecastAccess(listener_id = new_listener.id
            , max_listeners = new_user_licences_num
            , expiration_date = datetime.strptime(new_user_exp_date, '%Y-%m-%d'))
            self.request.dbsession.add(new_listener_access)
        except DBAPIError:
            print("ojnonono")
            return HTTPFound(location = '/') #zamienic na jakis kod bledu, dodac log

        return Response(status_int = 200)
        