import configparser
import logging
import operator
from functools import reduce  # forward compatibility for Python 3

import pymongo

import reader_util


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
config = configparser.ConfigParser()
config.sections()
print('-----------------')
config.read('FILE.INI')
print(config['DEFAULT']['w_path'])
w_path = config['DEFAULT']['w_path']  # файлы реадера и сендера
r_path = config['DEFAULT']['r_path']  # фалы ресивера и энкодера
dbclient = pymongo.MongoClient('localhost', 27017)
dbmy = dbclient["testdb"]
dbcollection = dbmy["reader1"]
config_d = config['DEFAULT'].getboolean('is_debug')
if config_d:
    dbcollection.drop()
f = open(w_path + "reader.log")
logger.info('Mongo end init')
list_doc = []
for line in f:
    list = line.split()
    if "main - INFO - Reader connected" in line:
        logger.info('Reader connected')
        print('')
        query = {}
        query["data"] = list[0]
        query["time"] = list[1]

        cursor = dbcollection.find_one(query)
        if cursor:  # есть уже
            list_doc.append(cursor)
            print(cursor)
        else:  # новый
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
            list_doc.append(doc_value[0])
            Sid = list[12]
        continue
    if "main - INFO - Reader disconnected." in line:
        logger.info('Reader Disconnected')
        query = {"Sid": list[12]}
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            newparam = {"$set": {"Disconnected": [{"Data": list[0], "Time": list[1]}]}}
            dbcollection.update_one(query, newparam)
            # работа с объектом
            for doc in list_doc:
                if doc["Sid"] in list[12]:
                    doc["Disconnected"] = {"Data": list[0], "Time": list[1]}
                    break
            else:
                print("Not found")
            Sid = None
        continue
    # вставлен флеш накопитель
    if "main - INFO - Flash drive connected to reader" in line:
        logger.info('Flash connected')
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
            # работа с объектом
            for doc in list_doc:
                if doc["Sid"] in list[19]:
                    doc["Flash_record"] = {"Connection": [{"Data": list[0], "Time": list[1]}], "No_AS": list[17],
                                           "No_Flash": "", }
                    break
            else:
                print("Not found")
            print(doc)
        continue
    if "Received data from shell: b'reading" in line:
        logger.info('Recive data')
        query["Flash_record.No_AS"] = No_AS
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            # создать новую коллекцию
            # TODO session
            logger.info('call a_log() %s', No_AS)
            #            reader_util.a_log(cursor['Sid'], No_AS, list[0], list[1])
            # добавить в основную коллекцию
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
            # работа с объектом
            for doc in list_doc:
                if doc.get("Flash_record") != None:
                    doc2 = getFromDict(doc, ["Flash_record", "No_AS"])
                    if doc2 in No_AS:
                        print(doc2)
                        doc["ReaderNoAS"] = {
                            "data": list[0],
                            "time": list[1],
                            "IP": list[10],
                            "No_AS": No_AS,
                            "Connected": list[1],
                            "Disconnected": ""
                        }

                    break
            else:
                print("No Record")
            dbcollection.update(query, doc_value)
            reader_util.a_log(cursor['Sid'], No_AS, list[0], list[1], w_path, r_path, dbcollection,list_doc)

        continue
    if "<e600812c>" in line:
        logger.info('Sender session trip')
        query = {}
        query["Session_record.No_Session"] = list[9]
        cursor = dbcollection.find_one(query)
        if cursor:
            tmpSid = cursor['Sid']
            query = {"Sid": tmpSid, "Session_record": {"$elemMatch": {"No_Session": list[9]}}}
            doc_value = {"$push": {"Session_record.$.Trip": {
                "Interval": {"Start": list[11],
                             "Finish": list[15]
                             },
                "Loco_ID": list[4],
                "Cabine_No": list[20],
                "Trip_No": "",
                "Global_No": "",
                "Log_Sender": list[22]}
            }
            }
            dbcollection.update(query, doc_value)
            # работа с объектом
            for doc in list_doc:
                if doc.get("Session_record"):
                    nosession=getFromDict(doc,["Session_record","No_Session"])
                    if nosession in list[9]:
                        print (nosession)

        continue
print("------finish--------")
