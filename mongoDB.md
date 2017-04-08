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

