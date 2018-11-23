
export MNAME=$1

mkdir /local/openLambda
cd /local/openLambda
git clone https://github.com/open-lambda/open-lambda.git
cd open-lambda

./quickstart/deps.sh
make test-all

./bin/admin new -cluster knapsack
./bin/admin workers -cluster=knapsack

cp -r ./quickstart/handlers/hello ./knapsack/registry/hello

wget https://www.emulab.net/downloads/geni-get.tar.gz
tar -zxvf geni-get.tar.gz
export WNAME=$(geni-get --all)$(geni-get --all | egrep -o "name=[\\][\"]worker-1(.*).uwmadison744-f18-PG0.wisc.cloudlab.us" | cut -c 17- | sed 's/.\{38\}$//')".uwmadison744-f18-PG0.wisc.cloudlab.us"

curl -X POST $MNAME/registerWorker -d '{"workerName": $WNAME}'