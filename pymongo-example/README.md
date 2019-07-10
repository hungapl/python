# Examples of using Pymongo
Useful examples of using pymongo to interact with a database that supports MongoDB API (including Azure CosmosDB):
- Persist data from Pandas dataframe into the database
- Search for data where the data filter given as a dict object
- Load search results from a database into a Panda dataframe
- Delete data from a collection given a data filter

## Setup
- Requires Python 3.6+
- Requires pymongo installed
- Requires MongoDB 2.3+ installed and running
- Requires a 'test' user created. Run the following commands in the console:

```
>> mongo
>> use admin
>> db.createUser( { user: "test", pwd: "test", roles: [ { role: "readWrite", db: "testdb" } ] } )
>> exit
```

## Examle and tests
- Refer to tests/db_test.py for examples
- Run db_test.py as unit test:
```
python3 -m unittest test.db_test
```