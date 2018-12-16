from multiprocessing import cpu_count, Pool
import requests
import time


def make_requests(args):
    path = args[0]
    count = args[1]
    for i in range(count):
        responseCode = 503
        while responseCode == 503:
            body = {}
            r = requests.post(path, json=body)
            print(r.content)
            responseCode = r.status_code
            time.sleep(.1)


processes = 5
request_count = 10
path = 'http://localhost/runLambda/step30'

pool = Pool(processes)
pool.map(make_requests, [(path, request_count)]*processes)
pool.terminate()