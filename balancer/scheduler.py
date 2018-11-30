import random


def schedule(workerList, path, post_data):
    return schedule__Random(workerList)

def schedule__Random(workerList):
    return random.choice(workerList)