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
