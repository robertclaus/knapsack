import random
import numpy as np
import server
from profileCalculator import insert_profile, getUsage, addUsage
from workerTracker import getTaskProfile

def schedule(workerList, task_id, post_data):
    #return schedule__Random(workerList, task_id)
    return schedule__withProfile(task_id, workerList)

def schedule__Random(workerList, task_id):
    worker = random.choice(workerList)
    #addUsage(worker, task_id)
    return worker


def schedule__withProfile(task_id, workerList):
    granularity = 0.01
    earliest_schedule_time_list = np.array(len(workerList))
    all_worker_usage = getUsage(granularity)
    task_profile = getTaskProfile(task_id)
    profile_interval = task_profile["interval"]
    cum_sum_profile_interval = np.cumsum(profile_interval)
    # ticks should have same dimension as profile_interval
    ticks = np.int(np.ceil(cum_sum_profile_interval/ granularity))
    profile_usage = np.empty(ticks[-1])
    for i in range(ticks):
        if i == 0:
            start = 0
        else:
            start = ticks[i-1]+1
        end = ticks[i]
        profile_usage[start:end] = profile_usage[start:end] + profile_interval[i]


    for i, each_worker in enumerate(workerList):
        earliest_schedule_time_list[i] = earliest_schedule_time(all_worker_usage[i], profile_usage)
    sorted_idx = np.argsort(earliest_schedule_time_list)
    addUsage(workerList[sorted_idx[0]], task_id)
    return workerList[0] if earliest_schedule_time_list[0] == 0 else None

def can_schedule(available_rss, required_rss):
    if available_rss.size != required_rss.size:
        print("two array should have same size")
    if np.all(available_rss-required_rss > 0):
        return True
    else:
        return False

def earliest_schedule_time(usage, profile):
    if usage.ndim > 1 | profile.ndim > 1:
        print("inputs should be 1d np arrary")
    available_rss = 1 - usage
    scope = available_rss.shape[0]+1
    available_rss_append = np.hstack((available_rss,np.ones(profile.shape[0])))
    
    # print(available_rss.shape)
    for shift in range(scope):
        if can_schedule(available_rss_append[shift:shift+profile.shape[0]], profile):
            return shift
       