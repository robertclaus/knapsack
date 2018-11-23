mkdir /local/openLambda
cd /local/openLambda
git clone https://github.com/open-lambda/open-lambda.git
cd open-lambda

./quickstart/deps.sh
make test-all

./bin/admin new -cluster knapsack
./bin/admin workers -cluster=knapsack

cp -r ./quickstart/handlers/hello ./knapsack/registry/hello

