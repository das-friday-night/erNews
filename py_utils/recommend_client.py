import pyjsonrpc
from config import RECOMMEND_SERVER

uri = 'http://%s:%i' % (RECOMMEND_SERVER['HOST'], RECOMMEND_SERVER['PORT'])
client = pyjsonrpc.HttpClient(url=uri)

def getUserPreferenceModel(userID):
    return client.call('getUserPreferenceModel', userID)
