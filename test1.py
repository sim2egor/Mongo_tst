import configparser
from datetime import datetime

import pymongo


def run_reciver(No_Session):
    try:
        file_reciver=open(r_path+"receiver.log","rt")
    except Exception as err:
        print(err)
        return
    Start_Session= False
    for line in  file_reciver:
        list = line.split()
        if "941fd277" in line: #  Kiosk session is
            Start_Session =True
        if "973b3d09" in line and Start_Session: #сессия началась и трип создан
            print(line)
        if "0641d919" in line:
            Start_Session =False


    pass


def a_log(Sid, Num_AS, dat, tim):
    try:
        file = open(w_path + "reader_" + Num_AS + "log", "rt")
    except Exception as err:
        print('Error')
        return
    print(tim)
    is_good = False
    No_Session = ""
    t_start = datetime.strptime(tim, '%H:%M:%S,%f')
    for line in file:
        list = line.split()
        if not is_good:
            dat1 = datetime.strptime(dat, '%Y-%m-%d')
            dat2 = datetime.strptime(list[0], '%Y-%b-%d')
            if dat1 == dat2:
                t_end = datetime.strptime(list[1], '%H:%M:%S.%f')
                delta = (t_end - t_start)
                if delta.total_seconds() < 20:
                    print(delta.total_seconds())
                    is_good = True
                    continue
            file.close()
            return
        else:  # файл текущий
            if "50f95925" in line:
                list2 = (list[13]).split('/')
                print("-----------Start reading---------------")
                query = {}
                query = {"Sid": Sid}
                doc_value = {"$push": {"Session_record":
                                           {"No_AS": Num_AS,
                                            "No_Session": list2[3],
                                            "Connection": [{
                                                "Data": list[0],
                                                "Time": list[1]
                                            }]
                                            }
                                       }
                             }

                dbcollection.update(query, doc_value)
                No_Session = list2[3]
        if "9fa17e68" in line: # закончили чтение
            run_reciver(No_Session)
                                
config = configparser.ConfigParser()
config.sections()
print('-----------------')
config.read('FILE.INI')
print(config['DEFAULT']['w_path'])
w_path = config['DEFAULT']['w_path']#файлы реадера и сендера
r_path = config['DEFAULT']['r_path']#фалы ресивера и энкодера
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
