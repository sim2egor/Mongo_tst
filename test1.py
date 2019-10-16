import configparser
import logging
import operator
import threading
from datetime import datetime
from functools import reduce  # forward compatibility for Python 3

import pymongo


def run_reciver(no_session, r_path, dbcollection, list_doc, condition):  # работа с файлом ресивера    time_start = ""

    condition.acquire()
    try:
        file_receiver = open(r_path + "receiver.log", "rt")
    except Exception as err:
        print(err)
        return
    start_session = False
    condition.notify()
    condition.release()
    with condition:
        condition.wait()
    condition.acquire()
    logger.info("+++Start receiver")
    for line in file_receiver:
        list = line.split()
        if "941fd277" in line:  # Kiosk session is startet
            start_session = True
        if "<8797897123>" in line:
            time_start = list[9]
            time_finish = list[11]

        if "973b3d09" in line and start_session:  # сессия началась и трип создан
            query = {}
            query["Session_record.Trip.Interval.Start"] = time_start+"000" #time in microsec
            # query = {"Session_record": {
            #     "$elemMatch": {"no_session": no_session, "Trip": {"$elemMatch": {"Interval.Start": time_start}}}}}
            cursor = dbcollection.find(query)
            if cursor:
                logger.info("session trip match %s, %s",time_start,no_session)
                for doc in cursor:
                    print(doc)
        #                tmpSid = cursor['Sid']
        # query = {"Sid": tmpSid, "Session_record": {"$elemMatch": {"no_session": list[9]}}}
        # doc_value = {"$push": {"Session_record.$.Trip": {
        #     "Interval": {"Start": list[11],
        #                  "Finish": list[15]
        #                  },
        #     "Loco_ID": list[4],
        #     "Cabine_No": list[20],
        #     "Trip_No": "", ----------------------It is!!!!!!!add
        #     "Global_No": "",
        #     "Log_Sender": list[22]}
        # }
        # }
        #
        # dbcollection.update(query, doc_value)

        if "0641d919" in line:  # end Session
            start_session = False
            time_finish = ""
            time_start = ""
            # отрабатываем энкодер
    condition.notify()
    condition.release()
    pass


def a_log(sid, num_AS, dat, tim, w_path, r_path, dbcollection, list_doc, condition):
    try:
        file = open(w_path + "reader_" + num_AS + "log", "rt")
    except Exception as err:
        print('Error %1', err)
        return
    print(tim)
    is_good = False
    no_session = ""
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
            if "50f95925" in line:  # создание сессии
                list2 = (list[13]).split('/')
                print("-----------Start reading---------------")
                query = {}
                query = {"Sid": sid}
                doc_value = {"$push": {"Session_record":
                                           {"No_AS": num_AS,
                                            "no_session": list2[3],
                                            "Connection": [{
                                                "Data": list[0],
                                                "Time": list[1]
                                            }]
                                            }
                                       }
                             }

                dbcollection.update(query, doc_value)
                # работа с обьектом
                for doc in list_doc:
                    if doc["Sid"] in sid:
                        doc["Session_record"] = {"No_AS": num_AS,
                                                 "no_session": list2[3],
                                                 "Connection": [{
                                                     "Data": list[0],
                                                     "Time": list[1]
                                                 }]}
                no_session = list2[3]
        if "9fa17e68" in line:  # закончили чтение
            # reciver_util.run_reciver(no_session, r_path, dbcollection,list_doc)
            my_thread = threading.Thread(target=run_reciver,
                                         args=(no_session, r_path, dbcollection, list_doc, condition,))
            worker_list.append(my_thread)
            my_thread.start()
            logger.info(" new receiver thread")
pass


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


# mutex
condition = threading.Condition()
# закрыли mutex
condition.acquire()
worker_list = []
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log','w')
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
            no_AS = list[17]
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
        query["Flash_record.No_AS"] = no_AS
        cursor = dbcollection.find_one(query)
        if cursor is not None:
            # создать новую коллекцию
            # TODO session
            logger.info('call a_log() %s', no_AS)
            #            reader_util.a_log(cursor['Sid'], No_AS, list[0], list[1])
            # добавить в основную коллекцию
            doc_value = {"$push": {"ReaderNoAS":
                {
                    "data": list[0],
                    "time": list[1],
                    "IP": list[10],
                    "No_AS": no_AS,
                    "Connected": list[1],
                    "Disconnected": ""
                }
            }
            }
            # работа с объектом
            for doc in list_doc:
                if doc.get("Flash_record") != None:
                    doc2 = getFromDict(doc, ["Flash_record", "No_AS"])
                    if doc2 in no_AS:
                        print(doc2)
                        doc["ReaderNoAS"] = [{
                            "data": list[0],
                            "time": list[1],
                            "IP": list[10],
                            "No_AS": no_AS,
                            "Connected": list[1],
                            "Disconnected": ""
                        }]

                    break
            else:
                print("No Record")
            dbcollection.update(query, doc_value)
            a_log(cursor['Sid'], no_AS, list[0], list[1], w_path, r_path, dbcollection, list_doc, condition)

        continue
    if "<e600812c>" in line:
        logger.info('Sender session trip')
        query = {}
        query["Session_record.no_session"] = list[9]
        cursor = dbcollection.find_one(query)
        if cursor:
            tmpSid = cursor['Sid']
            query = {"Sid": tmpSid, "Session_record": {"$elemMatch": {"no_session": list[9]}}}
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
                    nosession = getFromDict(doc, ["Session_record", "no_session"])
                    if nosession in list[9]:
                        print(nosession)
    if "sender: <bd2906f4>" in line:  # sender: <bd2906f4> Successfully connected with receiver at 127.0.0.1:7002
        logger.info("sender connected to server")
        condition.notify()
        condition.release()
        continue

for cond in worker_list:
    cond.join()
print("------finish--------")
