from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse, json
import requests
import imp

from scheduler import Scheduler
from profileCalculator import ProfileCalculator

from collections import defaultdict



class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    registeredWorkers = []
    profileData = defaultdict(list)
    calculatedProfile = defaultdict(list)

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
            self._set_headers()
            self.wfile.write("Received data for worker {}:\r\n{}".format(post_data.get('workerName'), post_data))
        elif "/profileData" in parsed_path.path:
            self._set_headers()
            self.wfile.write("All profile data:\r\n{}".format(MyHTTPRequestHandler.profileData))
        elif "/calculateProfile" in parsed_path.path:
            imp.reload(ProfileCalculator)
            MyHTTPRequestHandler.calculatedProfile = ProfileCalculator.calculate(MyHTTPRequestHandler.profileData)

            self._set_headers()
            self.wfile.write("Calculated Profile {}".format(MyHTTPRequestHandler.calculatedProfile))
        elif "/runLambda" in parsed_path.path:
            imp.reload(Scheduler)
            selectedWorker = Scheduler.schedule(MyHTTPRequestHandler.registeredWorkers, parsed_path.path, post_data)

            path = "http://{}:8080{}".format(selectedWorker, parsed_path.path)
            request_data = post_data

            r = requests.post(path, json=request_data)
            self._set_headers(r.status_code)
            self.wfile.write(r.text)
        elif "/status" in parsed_path.path:
            response = ""
            for worker in MyHTTPRequestHandler.registeredWorkers:
                r = requests.post("http://{}:8080{}".format(worker, parsed_path.path), json=post_data)
                response += "\r\n\r\n{}:\r\n{}\r\n".format(worker, r.text)
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
