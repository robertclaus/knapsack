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
Check for any process using 8080: netstat -ltnp
Kill the workers cleanly if possible and reset the entire cluster:

sudo ./bin/admin kill -cluster=knapsack
sudo rm -r knapsack/
sudo ./bin/admin new -cluster knapsack
sudo ./bin/admin setconf --cluster=knapsack "{\"startup_pkgs\":[\"requests\", \"multiprocessing\", \"numpy\"]}"
sudo ./bin/admin workers -cluster=knapsack -n 50
sudo cp -r ./quickstart/handlers/hello ./knapsack/registry/hello
sudo cp -r ./lambdas/* ./knapsack/registry/
sudo chmod -R +777 knapsack/

