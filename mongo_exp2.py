# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["demo"]
collection = db["test_collection"]

db.inventory.insert_many([
    {"item": "canvas",
     "qty": 100,
     "size": {"h": 28, "w": 35.5, "uom": "cm"},
     "status": "A"},
    {"item": "journal",
     "qty": 25,
     "size": {"h": 14, "w": 21, "uom": "cm"},
     "status": "A"},
    {"item": "mat",
     "qty": 85,
     "size": {"h": 27.9, "w": 35.5, "uom": "cm"},
     "status": "A"},
    {"item": "mousepad",
     "qty": 25,
     "size": {"h": 19, "w": 22.85, "uom": "cm"},
     "status": "P"},
    {"item": "notebook",
     "qty": 50,
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "status": "P"},
    {"item": "paper",
     "qty": 100,
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "status": "D"},
    {"item": "planner",
     "qty": 75,
     "size": {"h": 22.85, "w": 30, "uom": "cm"},
     "status": "D"},
    {"item": "postcard",
     "qty": 45,
     "size": {"h": 10, "w": 15.25, "uom": "cm"},
     "status": "A"},
    {"item": "sketchbook",
     "qty": 80,
     "size": {"h": 14, "w": 21, "uom": "cm"},
     "status": "A"},
    {"item": "sketch pad",
     "qty": 95,
     "size": {"h": 22.85, "w": 30.5, "uom": "cm"},
     "status": "A"}])
db.inventory.update_many(
    {"qty": {"$lt": 50}},
    {"$set": {"size.uom": "in", "status": "P"},
     "$currentDate": {"lastModified": True}})

db.inventory.replace_one(
    {"item": "paper"},
    {"item": "paper",
     "instock": [
         {"warehouse": "A", "qty": 60},
         {"warehouse": "B", "qty": 40}]})

db.inventory.drop()

# Subdocument key order matters in a few of these examples so we have
# to use bson.son.SON instead of a Python dict.
from bson.son import SON
db.inventory.insert_many([
    {"item": "journal",
     "instock": [
         SON([("warehouse", "A"), ("qty", 5)]),
         SON([("warehouse", "C"), ("qty", 15)])]},
    {"item": "notebook",
     "instock": [
         SON([("warehouse", "C"), ("qty", 5)])]},
    {"item": "paper",
     "instock": [
         SON([("warehouse", "A"), ("qty", 60)]),
         SON([("warehouse", "B"), ("qty", 15)])]},
    {"item": "planner",
     "instock": [
         SON([("warehouse", "A"), ("qty", 40)]),
         SON([("warehouse", "B"), ("qty", 5)])]},
    {"item": "postcard",
     "instock": [
         SON([("warehouse", "B"), ("qty", 15)]),
         SON([("warehouse", "C"), ("qty", 35)])]}])
# find in array
aaa=({"instock": SON([("qty",5)])})
cursor = db.inventory.find_one ({"instock": SON([("qty",5)])})
print(cursor)
query = {}
query["instock.warehouse"] = u"A"

cursor = db.inventory.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()
