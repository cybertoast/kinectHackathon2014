from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from werkzeug.serving import run_simple
# from werkzeug.wsgi import DispatcherMiddleware

from oscbridge import app as core_app

# app = core_app.create_app()

if __name__ == '__main__':
    # For aptana/eclipse debugging we need to do some meandering
    #    keep in mind that the middleware is a separate app from the flask-app
#     if app.debug:
#         use_debugger = True
#     try:
#         use_debugger = not(app.app.config.get('DEBUG_WITH_APTANA'))
#     except:
#         # Config is invalid, so use-debugger will be default
#         pass

    # Using tornado (non-blocking server)
#     http_server = HTTPServer(WSGIContainer(app))
#     http_server.listen(5000)
#     IOLoop.instance().start()
    
    run_simple('0.0.0.0',
               5000,
               core_app.create_app(),
               use_evalex=True)

