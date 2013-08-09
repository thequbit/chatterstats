from wsgiref.simple_server import make_server

from pyramid.config import Configurator

def main():
    config = Configurator()
    #config.add_view(index_view, route_name='/')
    #config.add_view(wordsjson, route_name='words.json')
    config.scan("views")
    config.add_static_view('static', 'static', cache_max_age=3600)
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
