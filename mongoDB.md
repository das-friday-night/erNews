sudo service mongod start
sudo service mongod stop
sudo service mongod restart

mongoimport --db test --collection restaurants --drop --file ~/downloads/primer-dataset.json
[link](https://docs.mongodb.com/getting-started/shell/import-data/)


# start mongo shell
$ mongo 

# display the database you are using, the operation should return test, which is the default database
$ db 

# switch databases
$ use <database> 

# list the available databases
$ show dbs

# list the available collection of current db
$ show collections

# creates both the database myNewDatabase and the collection myCollection
$ use myNewDatabase
$ db.myCollection.insertOne( { x: 1 } )

# create an empty collection in current db
$ db.createCollection("collection_name")

# remove All Documents from a Collection
$ db.collection_name.remove( { } )

## I/O files:
        **This commend need to run in shell not the mongo shell**
        - $ mongoexport --db <database-name> --collection <collection-name> --out output.json
        - $ mongoimport --db <database-name> --collection <collection-name> --file input.json

## Notes on pymongo
ans = db[collection].find()
* ans is a pymongo.cursor object. 
* to use it in python, we needs bson.json_util.dumps to convert it to str object.

```python
from bson import Binary, Code
from bson.json_util import dumps
dumps([{'foo': [1, 2]},
        {'bar': {'hello': 'world'}},
        {'code': Code("function x() { return 1; }", {})},
        {'bin': Binary(b"")}])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$code": "function x() { return 1; }", "$scope": {}}}, {"bin": {"$binary": "AQIDBA==", "$type": "00"}}]'

```

ans = db[collection].find_one()
* ans is a dict object. we can use it directly
