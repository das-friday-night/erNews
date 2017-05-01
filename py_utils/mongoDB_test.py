import mongoDB
import datetime
from dateutil import parser


x = mongoDB.getCollection()

tm = parser.parse("2017-04-29T11:43:33Z")
# parse news publish date
publishedTime = tm
publishedDayBegin = datetime.datetime(publishedTime.year, publishedTime.month, publishedTime.day, 0, 0, 0, 0)
publishedDayEnd = publishedDayBegin + datetime.timedelta(days=1)
ans = list(x.find({'publishedAt': {'$gte': publishedDayBegin, '$lt': publishedDayEnd}}))
print len(ans)
