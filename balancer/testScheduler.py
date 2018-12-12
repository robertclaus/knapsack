
import scheduler

registeredWorkers = ['myWorker']

workerToUse = scheduler.schedule(registeredWorkers, "/runLambda/step30", "")

assert workerToUse == 'myWorker'