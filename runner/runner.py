from multiprocessing import cpu_count, Pool
import requests


def make_requests(path, usages, intervals, count):
    for i in range(count):
        body = {"usages":usages, "intervals":intervals}
        r = requests.post(path, json=body)


usages = [.1,.9,.1]
intervals = [5,5,5]
processes = 10
request_count = 10
path = 'http://localhost/runLambda/steps'

pool = Pool(processes)
pool.map(make_requests, [(path, usages, intervals, request_count)]*processes)
pool.terminate()