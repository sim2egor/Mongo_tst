# Requires pymongo 3.6.0+
from pymongo import MongoClient
# Subdocument key order matters in a few of these examples so we have
# to use bson.son.SON instead of a Python dict.
from bson.son import SON

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

print("=========insert many===============")
coll=db["passport"]
coll.drop()
coll.insert_many([
    {"item": "journal",
     "status": "A",
     "size": {"h": 14, "w": 21, "uom": "cm"},
     "instock": [{"warehouse": "A", "qty": 5},]},
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
places_visited = [
    "Palace of Dob",
    "Palace of Victoria",
    "Sahara Desert"
]
coll.update({}, { "$set": { "Places Visited": places_visited } }, multi=True)

# show updated data
print("show update")
for doc in coll.find():
    print(doc)
print ("================================set=======================")
m1 =db["m1"]
query={}
query={"a":{"$elemMatch":{"a1.c1": "5656"}}}
cursor =m1.find_one(query)
doc={}
doc={"$set":{"a.$[].a.$[q1].c1":"444",
         "arrayFilters":[
        {
        "q1.c1":"5656"
        }
         ],"multi":"True"
    }
    }
m1.update_one({},{"$set":{"a.$[q0].a1.$[q1].c1":"444"}},array_filters=[{"q0.b1":"777"},{"q1.c1":"5656"}])
#db.posts.update_one({}, { '$set': { "arr1.$[el1].arr2.$[el2].arr3.$[el3].arr4.$[el4].someInfo": "123" } }, array_filters=[{'el1.id1': 'abc'},{'el2.id2': 'ijk'},{'el3.id3':'xyz'},{'el4.someInfo':'...'}])
for doc in m1.find():
    print(doc)

# db.posts.update_one({}, {'$set':{'arr1.$[element1].arr2.$[element2].arr3.$[elemenet3].arr4': {'id4': 'foo', 'someInfo': '!!!'},
#                               'arrayFilters': {'element1.id1': id1, 'element2.id2': id2, 'elemenet3.id3': id3}}}, True)
# db.posts.update_one({}, { '$set': { "arr1.$[el1].arr2.$[el2].arr3.$[el3].arr4.$[el4].someInfo": "here" } }, array_filters=[{'el1.id1': 'abc'},{'el2.id2': 'ijk'},{'el3.id3':'xyz'},{'el4.id4':'foo'}])
