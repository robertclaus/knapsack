# knapsack
A framework for learned smart-packing of tasks on OpenLambda.

## Install
Install the master first since the workers will auto-register themselves with the master.

### Master
1. Run: wget https://raw.githubusercontent.com/robertclaus/knapsack/master/deploy/master_setup.sh
2. Run: sudo bash master_setup.sh

### Workers
1. Run: wget https://raw.githubusercontent.com/robertclaus/knapsack/master/deploy/worker_setup.sh
2. Run: sudo bash worker_setup.sh [master hostname] [worker hostname]

For example:
sudo bash worker_setup.sh master.Knapsack05.uwmadison744-f18-PG0.wisc.cloudlab.us worker-3.Knapsack05.uwmadison744-f18-PG0.wisc.cloudlab.us


## Stopping/Resetting the servers

### Master
1. Run: ps -ef |grep nohup
2. Find the correct process ID and run: kill PID
3. cd /local
4. rm -r knapsack

### Workers
1. cd /local/openLambda/open-lambda
2. ./bin/admin kill -cluster=my-cluster
3. rm -r my-cluster
4. cd /local
5. rm -r openLambda