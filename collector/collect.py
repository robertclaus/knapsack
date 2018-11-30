import os
import pandas as pd

tempfilename = "tempdatafile.txt"
username = "anujagolechha"
resultfilename = "usage.csv"
delay = 0.01
niterations = 10

cmd = "top -u " + username + " -b -d " + str(delay) + " -n " + str(niterations) + " | awk '{print $1 \",\" $2 \",\" $12 \",\" $9 \",\" $10}' | awk '{ system(\"date +%s\"); print $0 }' > " + tempfilename
print cmd, type(cmd)
os.system(cmd)


# process data
f = open(tempfilename)
data = f.read()
data = data.split("\n")

l = []
n = len(data)
for i in range(0, n - 1, 2):
    currele = [data[i]]
    temp = data[i + 1]
    temp = temp.split(",")
    currele.extend(temp)
    l.append(currele[:])

# l - Timestamp, pid, user, cmd, cpu, mem

columns = {0:"Timestamp", 1:"PID", 2:"User", 3:"Cmd", 4:"CPU", 5:"Mem"}

df = pd.DataFrame(l)
df = df[range(6)]
df.rename(columns=columns, inplace=True)

df = df[df["PID"].apply(lambda x:x.isdigit())]
df = df.sort_values(["PID"])
df.reset_index(drop=True, inplace=True)
df.to_csv(resultfilename)