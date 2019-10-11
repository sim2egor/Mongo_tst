def run_reciver(No_Session, r_path, dbcollection):  # работа с файлом ресивера
    time_start = ""
    time_finish = ""
    try:
        file_reciver = open(r_path + "receiver.log", "rt")
    except Exception as err:
        print(err)
        return
    Start_Session = False
    for line in file_reciver:
        list = line.split()
        if "941fd277" in line:  # Kiosk session is startet
            Start_Session = True
        if "<8797897123>" in line:
            print(line)
            time_start = list[9]
            time_finish = list[11]

        if "973b3d09" in line and Start_Session:  # сессия началась и трип создан
            print("2")
            print(line)
            query = {}
            query = {"Session_record": {
                "$elemMatch": {"No_Session": No_Session, "Trip": {"$elemMatch": {"Interval.Start": time_start}}}}}
            cursor = dbcollection.find_one(query)
            if cursor:
                tmpSid = cursor['Sid']
                # query = {"Sid": tmpSid, "Session_record": {"$elemMatch": {"No_Session": list[9]}}}
                # doc_value = {"$push": {"Session_record.$.Trip": {
                #     "Interval": {"Start": list[11],
                #                  "Finish": list[15]
                #                  },
                #     "Loco_ID": list[4],
                #     "Cabine_No": list[20],
                #     "Trip_No": "",
                #     "Global_No": "",
                #     "Log_Sender": list[22]}
                # }
                # }
                #
                # dbcollection.update(query, doc_value)

        if "0641d919" in line:  # end Session
            Start_Session = False
            time_finish = ""
            time_start = ""
            # отрабатываем энкодер
    pass
