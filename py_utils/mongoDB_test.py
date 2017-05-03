import mongoDB
import datetime
import json
import bson.json_util as bson
from dateutil import parser


x = mongoDB.getPreferences()
y = list(x.find({'ss': 5 }))
print type(y) 
print len(y)
