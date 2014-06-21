from flask import request, Flask, jsonify
import os
import signal
import yaml
import sys
from time import sleep

# Export this function to the caller
__all__ = ['create_app']
APPNAME = 'Oscbridge'
queue = None

def create_app(app_name=None):
    if app_name is None:
        app_name = __name__
        
    app = Flask(app_name)
    app.url_map.strict_slashes = False

    if app.config.get('DEBUG') == True:
        app.debug = True

    configure_app(app)
    configure_signals()
    configure_sockets(app)
    configure_routes(app)
    configure_queue(app)
    configure_osc_receiver(app)
    
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
    global queue
    queue = Queue.Queue()

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
        global queue
        if not queue.empty():
#             OSCWebSocketHandler.send_updates(json.dumps({"msg": queue.get() }))
            # print queue.get()
            return jsonify(msg=queue.get())
            
#         return Response(sensor_stream(),
#                         mimetype='text/event-stream')

def configure_signals():
    signal.signal(signal.SIGINT, signal_handler)

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def configure_osc_receiver(app):
    """Set up the OSC receiver so that data can be sent to the websocket 
    """
    from OSC import OSCServer, ThreadingOSCServer
    from threading import Thread
    # funny python's way to add a method to an instance of a class
    import types
    
    # server = OSCServer( ("localhost", 5005) )
    from pdb import set_trace; set_trace()
    server = ThreadingOSCServer( ("localhost", 5005) )
    server.timeout = 0
    run = True
    
    # Add message handlers to server
    server.addMsgHandler( "/user/1", user_callback )
    server.addMsgHandler( "/user/2", user_callback )
    server.addMsgHandler( "/user/3", user_callback )
    server.addMsgHandler( "/user/4", user_callback )
    server.addMsgHandler( "/quit", quit_callback )
    
    server.addMsgHandler( "/test/1", osc_handler )
    
    # Start the server on a thread
    st = Thread( target = server.serve_forever )
    st.start()

    server.handle_timeout = types.MethodType(handle_timeout, server)
        
# --- osc stuff

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args[2],args[0],1-args[1]) 

def osc_handler( addr, tags, stuff, source):
    print addr, stuff
    global queue
    queue.put( [addr, stuff] )
        
def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()
