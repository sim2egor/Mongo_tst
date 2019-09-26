import pymongo, datetime
from pymongo import MongoClient

dbclient = pymongo.MongoClient('localhost', 27017)
dbmy = dbclient["testdb"]
dbcollection = dbmy["reader1"]
f = open("/diska/Log File/LOG-1.57/log reader sender/reader.log")
for line in f:
    list = line.split()
    if "main - INFO - Reader connected" in line:
        print('ok')
        query = {}
        query["data"] = list[0]
        query["time"] = list[1]

        cursor = dbcollection.find_one(query)
        if cursor:  # есть уже
            print(cursor)
        else:  # новый
            # bsoncxx::document::value
            doc_value = [{
                "data": list[0],
                "time": list[1],
                "IP": list[10],
                "Sid": list[12],
                "Connected": list[1],
                "Disconnected": ""
            }]
            dbcollection.insert(doc_value)
            Sid= list[12]

    if "main - INFO - Reader disconnected." in line:
        query = {"Sid": list[12]}
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            newparam = {"$set": {"Disconnected": list[1]}}
            dbcollection.update_one(query, newparam)
            Sid= None
    if "Received data from shell: b'reading" in line:
     query={"Sid":list[12]}
     cursor=dbcollection.find_one(query)
     if cursor is not None:
        newparam= {"$push":{
      "Time": list[1],
      "IP": list[12],
      "Rezult": list[11]
        }
        }
        dbcollection.update(query,newparam)
        # if (str.contains("Received data from shell: b'reading"))
        # {
        #     QList<QByteArray> data = line.split(' ');
        #     using builder::stream::array;
        #     using builder::stream::document;
        #
        #     using builder::stream::close_array;
        #     using builder::stream::close_document;
        #     using builder::stream::open_array;
        #     using builder::stream::open_document;
        #
        #     collection.find_one_and_update(bsoncxx::builder::stream::document{}
        #                                        << "Sid" << Sid
        #                                        << bsoncxx::builder::stream::finalize,
        #                                    bsoncxx::builder::stream::document{}
        #                                        << "$push" << open_document << "modify" << open_document << "Time" << data[1].toStdString() << "IP" << data[12].toStdString() << "Result" << data[11].toStdString() << close_document << close_document
        #
        #
        #

# dat=[
#  { "id":110, "data":{"Country":"ES","Count":64}},
#  { "id":112, "data":{"Country":"ES","Count":5}},
#  { "id":114, "data":{"Country":"UK","Count":3}},
#  {"datestamp":datetime.datetime.utcnow()}
# ]
# dbcollection.insert(dat)
