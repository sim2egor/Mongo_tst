# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
database = client["demo"]
collection = database["test_collection"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = {}
query["data.Country"] = u"ES"
set1 = {
    "$push": {"aaa": 1, "bbb": 2}
}
collection.update(query, set1)
cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()
