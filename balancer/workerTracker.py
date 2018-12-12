import sqlite3
import const
import datetime
from collections import defaultdict

def init(workers):
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_log(worker TEXT, port INT, task TEXT, timestamp timestamp, state INT);''')
    db.commit()

    db.close()


def worker_start(worker, port, task, timestamp):
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute('''INSERT INTO task_log(worker, port, task, timestamp, state) VALUES(?,?,?,?,?)''', (worker, port, task, timestamp, 0))
    db.commit()

    db.close()

def worker_end(worker, port, task, timestamp):
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute('''INSERT INTO task_log(worker, port, task, timestamp, state) VALUES(?,?,?,?,?)''', (worker, port, task, timestamp, 1))
    db.commit()

    db.close()

def port_to_use(worker):
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute("SELECT port, state FROM task_log WHERE worker='"+worker+"' AND timestamp!='None' ORDER BY timestamp DESC")

    closedPorts = defaultdict(lambda: False)
    all_rows = cursor.fetchall()
    for row in all_rows:
        if closedPorts[row[0]] or row[1] == 0:
            closedPorts[row[0]]=True
            continue
        return row[0]

    for port in const.ports:
        if not closedPorts[port]:
            return port

    print("No ports available")

    db.close()

    return None


def getTaskProfile(task):
    if task == '/runLambda/step30':
        return {"interval":[2.0, 7.0, 1.0],
                "usage":[0.05, 0.3, 0.05]}

    if task == '/runLambda/step60':
        return {"interval":[2.0, 7.0, 1.0],
                "usage":[0.05, 0.6, 0.05]}

    if task == '/runLambda/stepShort80':
        return {"interval":[1.25, 1.5, 0.25],
                 "usage":[0.05, 0.8, 0.05]}

    return {"interval":[1],
            "usage":[0.5]}

def running_tasks():
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute("SELECT worker, port, task, timestamp, state FROM task_log WHERE timestamp!='None' ORDER BY timestamp ASC")

    ongoingTasks = defaultdict(lambda: None)
    all_rows = cursor.fetchall()
    for row in all_rows:
        state = row[4]
        port = row[1]
        task = row[2]
        start = row[3]
        worker = row[0]

        if state == 1:
            #Consider any tasks on this port closed
            ongoingTasks[port] = None
        if state == 0:
            # Add task as active IF timestamp was recent enough
            if start > datetime.datetime.now() - datetime.timedelta(minutes=5):
                taskProfile = getTaskProfile(task)
                taskData = {"task":task,
                            "start":start,
                            "end":start + datetime.timedelta(seconds=sum(taskProfile['interval'])),
                            "port":port,
                            "worker":worker}
                taskData.update(taskProfile)
                ongoingTasks[port] = taskData


    listOfTasks = []
    for port in const.ports:
        if ongoingTasks[port] is not None:
            listOfTasks.append(ongoingTasks[port])

    db.close()

    return listOfTasks
