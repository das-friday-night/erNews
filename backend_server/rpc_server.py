import sys
import os
import pyjsonrpc
import yaml
import rpc_server_util as util

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
RPC_SERVER = config['RPC_SERVER']
SERVER_HOST = RPC_SERVER['HOST']
SERVER_PORT = RPC_SERVER['PORT']

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        """Test method"""
        return a + b

    @pyjsonrpc.rpcmethod
    def getNews(self, userID, pageID):
        return util.getNews(userID, pageID)

    @pyjsonrpc.rpcmethod
    def logNewsClick(self, userID, newsID):
        return util.logNewsClick(userID, newsID)

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://%s:%d" % (SERVER_HOST, SERVER_PORT)
http_server.serve_forever()
