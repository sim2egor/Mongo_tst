# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client["testdb"]
collection = database["reader1"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = {}
query["Session_record"] = {
    u"$elemMatch": {
        u"No_Session": u"2834",
        u"Trip": {
            u"$elemMatch": {
                u"Interval.Start": u"1538704040000"
            }
        }
    }
}


cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()
