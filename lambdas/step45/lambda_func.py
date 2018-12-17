

from multiprocessing import cpu_count, Pool
import time
import numpy as np
import json
import math

def handler(event):
    # sample predefined profile
    interval_len = np.array([0.4,0.1,2])
    usage_lvl = np.array([0.01, 0.45, 0.01])
    min_iterations = np.array([0.0, 17.8, 0.0])

    try:
        applyPredefinedProfile(interval_len, usage_lvl, min_iterations)
    except Exception as e:
        return {'error': str(e)}


def spin_and_sleep(arg):
    granularity = 0.1
    percent = arg[0]/1.0
    interval = arg[1]/1.0
    min_iterations = math.pow(2,arg[2]/1.0)

    t_start = time.time()
    iterations = 0
    a = 1
    while time.time()-t_start < interval or iterations < min_iterations:
        t0_start = time.time()
        while time.time()-t0_start < granularity*percent:
            a=a*2 #busy
            iterations+=1
        time.sleep(granularity*(1.0-percent))

def set_cpu_usage_2(percent, interval, min_iterations):
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(spin_and_sleep, [(percent, interval, min_iterations)]*processes)
    pool.terminate()
   
def applyPredefinedProfile(interval_len, usage_lvl, min_iterations):
    if(interval_len.shape[0] != usage_lvl.shape[0]):
        print("interval size and usage level size should agree")
    for i in range(interval_len.shape[0]):
        set_cpu_usage_2(usage_lvl[i], interval_len[i], min_iterations[i])