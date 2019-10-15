# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["demo"]
collection = db["inventory"]
db.inventory.insert_many([
    {"item": "journal",
     "status": "A",
     "size": {"h": 14, "w": 21, "uom": "cm"},
     "instock": [{"warehouse": "A", "qty": 5}]},
    {"item": "notebook",
     "status": "A",
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "instock": [{"warehouse": "C", "qty": 5}]},
    {"item": "paper",
     "status": "D",
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "instock": [{"warehouse": "A", "qty": 60}]},
    {"item": "planner",
     "status": "D",
     "size": {"h": 22.85, "w": 30, "uom": "cm"},
     "instock": [{"warehouse": "A", "qty": 40}]},
    {"item": "postcard",
     "status": "A",
     "size": {"h": 10, "w": 15.25, "uom": "cm"},
     "instock": [
         {"warehouse": "B", "qty": 15},
         {"warehouse": "C", "qty": 35}]}])
cursor = db.inventory.find({"status": "A"})
for doc in cursor:
    print(doc)
print("==============================")
cursor = db.inventory.find(
    {"status": "A"}, {"item": 1, "status": 1})
for doc in cursor:
    print(doc)
print("==============================")
cursor = db.inventory.find(
    {"status": "A"},
    {"item": 1, "status": 1, "instock": {"$slice": -1}})
for doc in cursor:
    print(doc)

print(cursor)