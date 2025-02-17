def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('icecast_listener_add', '/icecast/listener/add')
    config.add_route('icecast_listener_remove', '/icecast/listener/remove')
    config.add_route('icecast_listener_register', '/icecast/listener/manage/register')
    config.add_route('icecast_listener_unregister', '/icecast/listener/manage/unregister')