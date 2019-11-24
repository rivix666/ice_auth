def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('not_found_404', '/')
    config.add_route('icecast_listener_add', '/icecast/listener/add')
    config.add_route('icecast_listener_remove', '/icecast/listener/remove')
