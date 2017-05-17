import sys
import os
import operator
from warnings import warn
import yaml
import pyjsonrpc
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'py_utils'))
from mongoDB import getPreferences

f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
RECOMMEND_SERVER = config['RECOMMEND_SERVER']
SERVER_HOST = RECOMMEND_SERVER['HOST']
SERVER_PORT = RECOMMEND_SERVER['PORT']
MAX_VALUE = RECOMMEND_SERVER['MAX_PREFER_RATIO']

# Ref: https://www.python.org/dev/peps/pep-0485/#proposed-implementation
# Ref: http://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def getUserPreferenceModel(self, userID):
        preferenceModel = list(getPreferences().find({'userID' : userID}))
        if len(preferenceModel) > 1:
            warn('''one user can only have one preference model in database. 
                    something wrong with the preference model''')
            return None
        elif len(preferenceModel) == 0:
            print '''recommend_server can't find user's preference'''
            return None
        else:
            print 'recommend_server find preference model for user: %s' % userID
            preferenceModel = preferenceModel[0]

            # convert a dict to list by sorting the value of news class from high to low
            sorted_tuples = sorted(preferenceModel['preference'].items(), key=operator.itemgetter(1), reverse=True)
            sorted_list = [x[0] for x in sorted_tuples]
            sorted_value_list = [x[1] for x in sorted_tuples]

            # for a sorted list, if the first preference is same as the last one
            # the preference makes no sense.
            if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
                warn('''first preference = last preference: something wrong with
                %s preference model''' % userID)
                return None

            # modify sorted_value_list to a ratio list in int
            minValue = min(sorted_value_list)
            value_ratio_list = []
            for value in sorted_value_list:
                value = int(value/minValue)
                # ternary_operators
                # https://eastlakeside.gitbooks.io/interpy-zh/content/ternary_operators/ternary_operators.html
                value if value < MAX_VALUE else MAX_VALUE
                value_ratio_list.append(value)

            return sorted_list,value_ratio_list

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://%s:%d" % (SERVER_HOST, SERVER_PORT)
http_server.serve_forever()