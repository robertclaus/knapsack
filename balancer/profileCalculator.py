import sqlite3
import const
from collections import defaultdict

def calculate(dataFile):
    insert_profile("test", 0, 100)


def insert_profile(task, timestamp, cpu):
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS calculated_profiles(task TEXT, timeoffset INT, cpu INT);''')
    db.commit()

    cursor = db.cursor()
    cursor.execute('''INSERT INTO calculated_profiles(task, timeoffset, cpu) VALUES(?,?,?)''', (task,timestamp,cpu))
    db.commit()

    db.close()

def getUsage():
    return [0]

def addUsage(worker, task):
    taskProfile = getTaskProfiles()[task]