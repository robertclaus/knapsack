from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse, json
import requests
import imp

import scheduler
import profileCalculator
import workerTracker

import datetime

from collections import defaultdict

import sqlite3

import time


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    dataFile = "/tmp/KnapsackDB"
    registeredWorkers = []
    profileData = defaultdict(list)
    calculatedProfile = defaultdict(list)
    startEndTimes = [] # task number, start time, end time
    currentTaskNumber = 0 # increment at each handler call

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allowed-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        parsed_path = urlparse.urlparse(self.path)

        if self.headers.getheader('content-length'):
            content_len = int(self.headers.getheader('content-length'))
            post_body = self.rfile.read(content_len)
            post_data = json.loads(post_body)
        else:
            post_data = {}


        if '/registerWorker' in parsed_path.path:
            MyHTTPRequestHandler.registeredWorkers.append(post_data.get('workerName'))
            workerTracker.init(MyHTTPRequestHandler.registeredWorkers)
            self._set_headers()
            self.wfile.write("Workers:{}".format(MyHTTPRequestHandler.registeredWorkers))
        elif '/unregisterWorkers' in parsed_path.path:
            MyHTTPRequestHandler.registeredWorkers = []
            self._set_headers()
            self.wfile.write("Workers:{}".format(MyHTTPRequestHandler.registeredWorkers))
        elif '/viewWorkers' in parsed_path.path:
            self._set_headers()
            self.wfile.write("Workers:{}".format(MyHTTPRequestHandler.registeredWorkers))
        elif "/addToProfileData" in parsed_path.path:
            MyHTTPRequestHandler.profileData[post_data.get('workerName')].append(post_data)
            db = sqlite3.connect(MyHTTPRequestHandler.dataFile)
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS profile_data(worker TEXT, timestamp TEXT, pid TEXT, cmd TEXT, cpu TEXT, mem TEXT);
            ''')
            db.commit()

            cursor = db.cursor()
            cursor.execute('''INSERT INTO profile_data(worker, timestamp, pid, cmd, cpu, mem)
                  VALUES(?,?,?,?,?,?)''', (post_data.get('workerName'), post_data.get('Timestamp'), post_data.get('PID'), post_data.get('Cmd'), post_data.get('cpu'), post_data.get('mem')))
            db.commit()

            db.close()
            self._set_headers()
            self.wfile.write("Received data for worker {}:\r\n{}".format(post_data.get('workerName'), post_data))
        elif "/profileData" in parsed_path.path:
            db = sqlite3.connect(MyHTTPRequestHandler.dataFile)

            cursor = db.cursor()
            cursor.execute('''SELECT * FROM profile_data''')

            result = ""
            all_rows = cursor.fetchall()
            for row in all_rows:
                result += str(row)

            db.close()

            self._set_headers()
            self.wfile.write("All profile data:\r\n{}".format(result))
        elif "/calculateProfile" in parsed_path.path:
            #imp.reload(profileCalculator)
            MyHTTPRequestHandler.calculatedProfile = profileCalculator.calculate(MyHTTPRequestHandler.dataFile)

            db = sqlite3.connect(MyHTTPRequestHandler.dataFile)

            cursor = db.cursor()
            cursor.execute('''SELECT * FROM calculated_profiles''')

            result = ""
            all_rows = cursor.fetchall()
            for row in all_rows:
                result += str(row)

            db.close()

            self._set_headers()
            self.wfile.write("Calculated Profile {}".format(result))
        elif "/runLambda" in parsed_path.path:
            #imp.reload(scheduler)
            selectedWorker = scheduler.schedule(MyHTTPRequestHandler.registeredWorkers, parsed_path.path, post_data)

            port = workerTracker.port_to_use(selectedWorker)
            path = "http://{}:{}{}".format(selectedWorker, port, parsed_path.path)
            request_data = post_data

            # get name of handler
            tempindex = parsed_path.path.index("/runLambda") + len("/runLambda")
            tempname = parsed_path.path[tempindex:]
            templist = ["task" + str(self.currentTaskNumber) + "_" + tempname, None, None]

            # store start time for current task
            templist[1] = int(time.time())

            workerTracker.worker_start(selectedWorker,port, parsed_path.path, datetime.datetime.now())
            r = requests.post(path, json=request_data)
            workerTracker.worker_end(selectedWorker,port, parsed_path.path, datetime.datetime.now())

            # store end time for current task
            templist[2] = int(time.time())

            # increment currentTaskNumber
            self.currentTaskNumber += 1

            # TODO
            # manage times in case of concurrent calls to multiple handlers

            self._set_headers(r.status_code)
            self.wfile.write(r.text)
        elif "/status" in parsed_path.path:
            response = ""
            for worker in MyHTTPRequestHandler.registeredWorkers:
                r = requests.post("http://{}:8080{}".format(worker, parsed_path.path), json=post_data)
                response += "\r\n\r\n{}:\r\n{}\r\n".format(worker, r.text)
            self._set_headers()
            self.wfile.write(response)
        elif "/lambdaStats" in parsed_path.path:
            response = ""
            response += json.dumps(startEndTimes)
            
            self._set_headers()
            self.wfile.write(response)
        else:
            self._set_headers()
            self.wfile.write("Not a recognized path")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run(server_class=ThreadedHTTPServer, handler_class=MyHTTPRequestHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
