# Requires pymongo 3.6.0+
from pymongo import MongoClient
import pprint


client = MongoClient('localhost', 27017)
db = client["demo"]
db.drop_collection("posts")
diction = {
  "arr1": [
    {
      "id1": "abc",
      "someInfo1": "...",
      "someInfo2": "...",
      "someInfo3": "...",
      "someInfo4": "...",
      "arr2": [
        {
          "id2": "ijk",
          "arr3": [
            {
              "id3": "xyz",
              "someInfo1": "...",
              "someInfo2": "...",
              "arr4": [
                {
                "id4": "foo",
                "someInfo": "..."
                },
                {
                "id4": "bar",
                "someInfo": "..."
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
db.posts.insert_one(diction)
db.posts.update_one({}, { '$set': { "arr1.$[el1].arr2.$[el2].arr3.$[el3].arr4.$[el4].someInfo": "123" } }, array_filters=[{'el1.id1': 'abc'},{'el2.id2': 'ijk'},{'el3.id3':'xyz'},{'el4.someInfo':'...'}])