import sqlite3

def calculate(dataFile):
    db = sqlite3.connect(dataFile)

    cursor = db.cursor()
    cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS calculated_profiles(timestamp TEXT, pid TEXT, cmd TEXT, cpu TEXT, mem TEXT);
                                ''')
    db.commit()

    cursor = db.cursor()
    cursor.execute('''INSERT INTO calculated_profiles(timestamp, pid, cmd, cpu, mem)
                      VALUES(?,?,?,?,?)''', ("1","2","3","4","5"))
    db.commit()