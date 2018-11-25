

export MNAME=$1
export WNAME=$2

curl -d '{"workerName":"$WNAME"}' $MNAME/registerWorker
