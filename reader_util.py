from datetime import datetime
import threading

import reciver_util


def a_log(Sid, Num_AS, dat, tim, w_path, r_path, dbcollection, list_doc, condition):
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
            if "50f95925" in line:  # создание сессии
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
                #работа с обьектом
                for doc in list_doc:
                    if doc["Sid"] in Sid:
                        doc["Session_record"]={"No_AS": Num_AS,
                                            "No_Session": list2[3],
                                            "Connection": [{
                                                "Data": list[0],
                                                "Time": list[1]
                                            }]}
                No_Session = list2[3]
        if "9fa17e68" in line:  # закончили чтение
            #reciver_util.run_reciver(No_Session, r_path, dbcollection,list_doc)
            my_thread = threading.Thread(target=reciver_util.run_reciver, args=(No_Session, r_path, dbcollection, list_doc, condition,))
            my_thread.start()
pass
