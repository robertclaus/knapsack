import sqlite3
import const
from collections import defaultdict
import numpy as np
import time

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
    granularity = 0.01 # unit in sec
    current_timestamp = time.time()
    active_profiles = getActiveTaskProfiles(current_timestamp)
    [usage, interval] = cal_total_usage(active_profiles, current_timestamp, granularity)

# each profile is in the form of {'start', 'end', 'usage', 'interval'}

def cal_total_usage(active_profiles, current_timestamp, granularity):
    max_task_length = 20 # maximum task length, unit second
    total_usage = np.array([0]* max_task_length/granularity)

    for each_profile_obj in active_profiles:
        add_to_usage(total_usage, each_profile_obj, current_timestamp)

    return usage, interval

def add_to_usage(total_usage, each_profile_obj, current_timestamp, granularity):
    # each profile here starts earlier than current timestamp and ends later than current timestamp
    profile_start = each_profile_obj[0]
    profile_end = each_profile_obj[1]
    profile_usage = each_profile_obj[2]
    profile_interval = each_profile_obj[3]
    tmp_timestamp = profile_start
    aligned_interval = None
    aligned_usage = None
    for i in range(profile_interval.shape[0]):
        tmp_timestamp = tmp_timestamp + profile_interval[i]
        if  tmp_timestamp < current_timestamp:
            continue
        else:
            aligned_interval = np.array([tmp_timestamp - current_timestamp])
            aligned_usage = profile_usage[i]
            aligned_interval.append(profile_interval[i+1: -1])
            aligned_usage.append(profile_usage[i+1: -1])
    # convert aligned_usage and aligned_interval to the form needed for sceduler
    total_interval_len = sum(aligned_interval)
    total_ticks = np.int(np.ceil(total_interval_len/ granularity))




def addUsage(worker, task):
    taskProfile = getTaskProfiles()[task]