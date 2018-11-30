import random

class Scheduler():
    def schedule(workerList, path, post_data):
        return self._schedule__Random(workerList)

    def schedule__Random(workerList):
        return random.choice(workerList)