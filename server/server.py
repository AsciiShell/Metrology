import cherrypy


class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def calc(self):
        return {"text": "here you should return metrics"}


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 8080,
        'tools.proxy.on': True,
    })
    cherrypy.quickstart(Root())
