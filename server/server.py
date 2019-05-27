import cherrypy


class Root(object):
    @cherrypy.expose
    def index(self):
        with open("index.html", 'r', encoding='utf8') as f:
            return f.read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def calc(self):
        return cherrypy.request.json


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'tools.proxy.on': True,
    })
    cherrypy.quickstart(Root())
