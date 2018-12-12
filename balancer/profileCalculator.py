import sqlite3
import const
from collections import defaultdict
import numpy as np
import time
from workerTracker import running_tasks
import datetime

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
    return cal_total_usage(current_timestamp, granularity)

# each profile is in the form of {'start', 'end', 'usage', 'interval'}

def cal_total_usage( current_timestamp, granularity):
    max_task_length = 20 # maximum task length, unit second
    total_usage = np.array([0]* np.int(max_task_length/granularity))
    active_profiles = running_tasks()
    for each_profile_obj in active_profiles:
        add_to_usage(total_usage, each_profile_obj, current_timestamp)

    return total_usage

def add_to_usage(total_usage, each_profile_obj, current_timestamp, granularity):
    # each profile here starts earlier than current timestamp and ends later than current timestamp
    profile_start_datetime = each_profile_obj["start"]
    profile_start = (profile_start_datetime - datetime.datetime.utcfromtimestamp(0)).total_seconds()

    profile_end = each_profile_obj["end"]
    profile_usage = each_profile_obj["usage"]
    profile_interval = each_profile_obj["interval"]
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
    cum_sum_profile_interval = np.cumsum(aligned_interval)
    ticks = np.int(np.ceil(cum_sum_profile_interval/ granularity))
    for i in range(ticks):
        if i == 0:
            start = 0
        else:
            start = ticks[i-1]+1
        end = ticks[i]
        total_usage[start:end] = total_usage[start:end] + aligned_usage[i]

    if(np.any(total_usage > 1.0)):
        print("Error")

def addUsage(worker, task):
    taskProfile = getTaskProfiles()[task]