mkdir /local/knapsack
cd /local/knapsack
git clone https://github.com/robertclaus/knapsack.git
cd knapsack


wget https://www.emulab.net/downloads/geni-get.tar.gz
tar -zxvf geni-get.tar.gz
export KNAME="master."$(geni-get --all | egrep -o "name=[\\][\"]worker-1(.*).uwmadison744-f18-PG0.wisc.cloudlab.us" | cut -c 17- | sed 's/.\{38\}$//')".uwmadison744-f18-PG0.wisc.cloudlab.us"

echo
echo
echo
echo $KNAME
echo
echo
echo

sudo nohup python ./balancer/server.py &

