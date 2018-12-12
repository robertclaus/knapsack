def handler(event):
    try:
        import os
        import pandas as pd
        import json

        tempfilename = "tempdatafile.txt"
        resultfilename = "usage.csv"
        delay = 0.01
        niterations = 3000

        cmd = "top -u root -b -d " + str(delay) + " -n " + str(niterations) + " | grep python | awk '{print $1 \",\" $2 \",\" $12 \",\" $9 \",\" $10}' | awk '{ system(\"date +%s\"); print $0 }' > " + tempfilename
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
        df = df.sort_values(["PID"]) # not really required any more

        # compression step, remove
        reqdIndices = []
        prevval = None

        n = len(df)
        for i in range(n):
            if df.iloc[i]["CPU"] != prevval:
                reqdIndices.append(i)
                prevval = df.iloc[i]["CPU"]

        df = df.iloc[reqdIndices]

        df.reset_index(drop=True, inplace=True)

        return json.dumps(df.to_csv())
    except Exception as e:
        return {'error': str(e)}
