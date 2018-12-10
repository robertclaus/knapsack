

from multiprocessing import cpu_count, Pool
import time
import numpy as np


def handler(event):
	rand_seed = 10
	interval = event[0]
	num_break_pt = 10
	# sample predefined profile
	interval_len = np.array([2]*8)
	usage_lvl = np.array([0.3,0.7]*4)
    try:
        applyRandomProfile(interval, rand_seed, num_break_pt)
        # applyPredefinedProfile(interval_len, usage_lvl)
    except Exception as e:
return {'error': str(e)} 



def spin_and_sleep(arg):
    granularity = 0.001 # 1ms
    # percent = 0.3
    percent = arg[0]
    interval = arg[1]
    t_start = time.clock()
    while time.clock()-t_start < interval:
        t0_start = time.clock()
        while time.clock()-t0_start < granularity*percent:
            2*2 #busy
        time.sleep(granularity*(1-percent))


def set_cpu_usage_2(percent, interval):
    processes = cpu_count()  
    pool = Pool(processes)
    pool.map(spin_and_sleep, [(percent, interval)]*processes)
    pool.terminate()


def applyRandomProfile(interval, rand_seed, num_break_pt):
    # generate a random perfoile for a certain interval
    np.random.seed(rand_seed)
    usage_lvl = np.random.rand(num_break_pt) 
    interval_len = np.random.rand(num_break_pt)
    interval_len = interval_len/sum(interval_len)*interval
    print("The random profile has following shape")
    print("usage_lvl: ", usage_lvl)
    print("interval_len: ", interval_len)
    for i in range(num_break_pt):
        set_cpu_usage_2(usage_lvl[i], interval_len[i])
   
def applyPredefinedProfile(interval_len, usage_lvl):
    if(interval_len.shape[0] != usage_lvl.shape[0]):
        print("interval size and usage level size should agree")
    for i in range(interval_len.shape[0]):
        set_cpu_usage_2(usage_lvl[i], interval_len[i])
        
