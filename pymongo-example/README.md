# Examples of using Pymongo
- Persist data from Pandas dataframe into a database that supports MongoDB API (including MongoDB and CosmosDB)
- Find and load data from a database into a Panda dataframe via MongoDB API

## Setup
- Requires Python 3.6+
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