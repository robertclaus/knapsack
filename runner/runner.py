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
            try:
                r = requests.post(path, json=body)
            except requests.exceptions.ConnectionError as errc:
                print("Connection Exception")
                continue
            print(r.content)
            responseCode = r.status_code
            time.sleep(.2)


processes = 10
request_count = 3
path = 'http://localhost/runLambda/per70'

pool = Pool(processes)
pool.map(make_requests, [(path, request_count)]*processes)
pool.terminate()