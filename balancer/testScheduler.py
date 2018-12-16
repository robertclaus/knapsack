
import scheduler

registeredWorkers = ['myWorker']

workerToUse = scheduler.schedule(registeredWorkers, "/runLambda/step30", "")
print(workerToUse)
assert workerToUse == 'myWorker'