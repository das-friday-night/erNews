import mongoDB
import datetime
import json
import bson.json_util as bson
from dateutil import parser


x = mongoDB.getCollection()

tm = parser.parse("2017-04-29T22:29:42Z")
# parse news publish date
publishedTime = tm
publishedDayBegin = datetime.datetime(publishedTime.year, publishedTime.month, publishedTime.day, 0, 0, 0, 0)
publishedDayEnd = publishedDayBegin + datetime.timedelta(days=1)
ans = x.find()
print type(bson.dumps(ans))
