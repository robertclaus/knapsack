

from multiprocessing import cpu_count, Pool
import time
import numpy as np
import json

def handler(event):
    intervals = event['intervals']
    usages = event['usages']
    # sample predefined profile
    interval_len = np.array(json.loads(intervals))
    usage_lvl = np.array(json.loads(usages))

    try:
        applyPredefinedProfile(interval_len, usage_lvl)
    except Exception as e:
        return {'error': str(e)}


def spin_and_sleep(arg):
    granularity = 0.1
    percent = arg[0]
    interval = arg[1]/1.0
    t_start = time.time()
    a = 1
    while time.time()-t_start < interval:
        t0_start = time.time()
        while time.time()-t0_start < granularity*percent:
            a=a*2 #busy
        time.sleep(granularity*(1.0-percent))

def set_cpu_usage_2(percent, interval):
    processes = cpu_count()
    pool = Pool(processes)
    pool.map(spin_and_sleep, [(percent, interval)]*processes)
    pool.terminate()
   
def applyPredefinedProfile(interval_len, usage_lvl):
    if(interval_len.shape[0] != usage_lvl.shape[0]):
        print("interval size and usage level size should agree")
    for i in range(interval_len.shape[0]):
        set_cpu_usage_2(usage_lvl[i], interval_len[i])