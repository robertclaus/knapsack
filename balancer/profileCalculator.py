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

def getTaskProfiles():
    db = sqlite3.connect(const.dataFile, detect_types=sqlite3.PARSE_DECLTYPES)

    cursor = db.cursor()
    cursor.execute('''SELECT task, timeoffset, cpu FROM profile_data''')

    result = defaultdict(list)

    all_rows = cursor.fetchall()
    for row in all_rows:
        result[row[0]].append((row[1],row[2]))

    db.close()

    for key,value in result:
        value.sort(key=lambda x: x[0], reverse=True)
        map(lambda x: x[1], value)

    return result

def getUsage():
    return [0]

def addUsage(worker, task):
    taskProfile = getTaskProfiles()[task]
    '''insert or replace into Book (ID, Name, TypeID, Level, Seen) values (
   (select ID from Book where Name = "SearchName"),
   "SearchName",
    5,
    6,
    (select Seen from Book where Name = "SearchName"));'''