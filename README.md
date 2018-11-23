# knapsack
A framework for learned smart-packing of tasks on OpenLambda.

## Install
Install the master first since the workers will auto-register themselves with the master.

### Master
1. Run: wget https://raw.githubusercontent.com/robertclaus/knapsack/master/deploy/master_setup.sh
2. Run: sudo bash master_setup.sh
3. This will print a master hostname towards the end that you will need to copy paste for the worker setup.

### Workers
1. Run: wget https://raw.githubusercontent.com/robertclaus/knapsack/master/deploy/worker_setup.sh
2. Run: sudo bash worker_setup.sh <master hostname>