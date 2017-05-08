import pyjsonrpc
import os
import yaml
f = open(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
config = yaml.load(f)
f.close()
RECOMMEND_SERVER = config['RECOMMEND_SERVER']

uri = 'http://%s:%i' % (RECOMMEND_SERVER['HOST'], RECOMMEND_SERVER['PORT'])
client = pyjsonrpc.HttpClient(url=uri)

def getUserPreferenceModel(userID):
    return client.call('getUserPreferenceModel', userID)
