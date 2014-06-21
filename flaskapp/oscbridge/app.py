from flask import request, Flask
import os
import yaml

# Export this function to the caller
__all__ = ['create_app']
APPNAME = 'Oscbridge'

def create_app(app_name=None):
    if app_name is None:
        app_name = __name__
        
    app = Flask(app_name)
    app.url_map.strict_slashes = False

    if app.config.get('DEBUG') == True:
        app.debug = True

    configure_app(app)
    configure_sockets(app)
    configure_routes(app)
    configure_queue(app)
    configure_osc_receiver()
    
    return app

def configure_app(app, configfile=None):
    """Initialize configuration files"""
    if not configfile:
        # The default config path is ./<appname>/config/*.yml, but it really
        # could be anything you want!
        configfile = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  "config",
                                  "config.yml")

    app.settings = yaml.load(file(configfile))
    # The Flask-common configurations are within the FLASK: definition
    app.config.update(app.settings.get('FLASK'))


def configure_queue(app):
    import Queue
    with app.app_context():
        app.queue = Queue.Queue()

def configure_sockets(app):
    from flask_sockets import Sockets
    app.sockets = Sockets(app)

def sensor_stream():
    count = 0
    while True:
        gevent.sleep(2)
        yield 'data: %s\n\n' % count
        count += 1
        
def configure_routes(app):
    @app.sockets.route('/echo')
    def echo_socket(ws):
        while True:
            message = ws.receive()
            ws.send(message)

    @app.route('/')
    def hello():
        return 'Hello World!'
    
    @app.sockets.route('/kinect')
    def kinect_stream():
        """Pass data from OSC receiver back through the socket
        """
        if not app.queue.empty():
#             OSCWebSocketHandler.send_updates(json.dumps({"msg": queue.get() }))
            print app.queue.get()
            
#         return Response(sensor_stream(),
#                         mimetype='text/event-stream')

def configure_osc_receiver():
    """Set up the OSC receiver so that data can be sent to the websocket 
    """
    from .modules.osc import receiver
    receiver.listen()
    