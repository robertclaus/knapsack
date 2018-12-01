import random
import numpy as np
import server


def schedule(workerList, path, post_data):
    # return schedule__Random(workerList)
    return schedule__withProfile(task_id, workerList, task_profile, usage_profile)

def schedule__Random(workerList):
    return random.choice(workerList)

def schedule__withProfile(task_id, workerList):
    earliest_schedule_time_list = np.array(workList.size())
    for i, each_worker in enumerate(workerList):
        earliest_schedule_time_list[i] = earliest_schedule_time(server.getUsage(), server.getProfile());
    sorted_idx = np.argsort(earliest_schedule_time_list)
    return workerList[sorted_idx[0]]

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
       