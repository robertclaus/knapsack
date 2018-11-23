
export WNAME=$1

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
export KNAME=$(geni-get --all | egrep -o "name=[\\][\"]$(geni-get client_id).*[.]us[\\][\"]" | cut -c 8- | sed 's/.\{2\}$//')

curl -X POST $MNAME/registerWorker -d '{"workerName": $WNAME}'