import pyjsonrpc
import sys
sys.path.append("..")
import py_utils.mongoDB as mongoDB
from py_utils.config import RPC_SERVER

SERVER_HOST = RPC_SERVER['HOST']
SERVER_PORT = RPC_SERVER['PORT']

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        """Test method"""
        return a + b

    @pyjsonrpc.rpcmethod
    def getNews(self):
        return mongoDB.getNews()

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://%s:%d" % (SERVER_HOST, SERVER_PORT)
http_server.serve_forever()