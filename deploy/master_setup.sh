mkdir /local/knapsack
cd /local/knapsack
git clone https://github.com/robertclaus/knapsack.git
cd knapsack


wget https://www.emulab.net/downloads/geni-get.tar.gz
tar -zxvf geni-get.tar.gz
export KNAME=$(geni-get --all | egrep -o "name=[\\][\"]$(geni-get client_id).*[.]us[\\][\"]" | cut -c 8- | sed 's/.\{2\}$//')

echo
echo
echo
echo $KNAME
echo
echo
echo

nohup python ./balancer/server.py &

