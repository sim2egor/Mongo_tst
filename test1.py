import pymongo, datetime
from pymongo import MongoClient

dbclient = pymongo.MongoClient('localhost', 27017)
dbmy = dbclient["testdb"]
dbcollection = dbmy["reader1"]
config_d = config['DEFAULT'].getboolean('is_debug')
if config_d:
    dbcollection.drop()
f = open(w_path + "reader.log")
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
                "No_AS": "",
                "IP": list[10],
                "Sid": list[12],
                "Connection": [{
                    "Data": list[0],
                    "Time": list[1]
                }]

            }]
            dbcollection.insert(doc_value)
            Sid = list[12]

    if "main - INFO - Reader disconnected." in line:
        query = {"Sid": list[12]}
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            newparam = {"$set": {"Disconnected": [{"Data": list[0], "Time": list[1]}]}}
            dbcollection.update_one(query, newparam)
            Sid = None
    if "main - INFO - Flash drive connected to reader" in line:
        query = {"Sid": list[19]}
        cursor = dbcollection.find_one(query)
        if cursor:
            newparam = {"$push": {
                'Flash_record': {"Connection": [{"Data": list[0], "Time": list[1]}], "No_AS": list[17],
                                 "No_Flash": "", }}}
            dbcollection.update(query, newparam)
            newparam = {"$set": {"No_AS": list[17]}}
            dbcollection.update(query, newparam)
            print(cursor)
            No_AS = list[17]
    if "Received data from shell: b'reading" in line:
        query["Flash_record.No_AS"] = No_AS
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            # создать новую коллекцию
            a_log(cursor['Sid'], No_AS, list[0], list[1])
            # добавить в основную коллекцию
            newparam = {"$push": {"Flash_2": {"Time": list[1], "IP": list[12], "Rezult": line}}}
            x = dbcollection.update(query, newparam)
            doc_value = {"$push": {"ReaderNoAS":
                {
                    "data": list[0],
                    "time": list[1],
                    "IP": list[10],
                    "No_AS": No_AS,
                    "Connected": list[1],
                    "Disconnected": ""
                }
            }
            }
            dbcollection.update(query, doc_value)
    if "<e600812c>" in line:
        query = {}
        query["Session_record.No_Session"] = list[9]
        cursor = dbcollection.find_one(query)
        if cursor:
            tmpSid=cursor['Sid']
            query={"Sid":tmpSid, "Session_record":{"$elemMatch":{"No_Session":list[9]}}}
            doc_value = {"$push": {"Session_record.$.Trip":{
                                            "Interval": { "Start" :list[11],
                                                           "Finish":list[15]
                                                           },
                                            "Loco_ID":list[4],
                                             "Cabine_No":list[20],
                                               "Trip_No":"",
                                               "Global_No":"",
                                            "Log_Sender": list[22]}
                                    }
                             }


            dbcollection.update(query,doc_value)

print("--------------")

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
