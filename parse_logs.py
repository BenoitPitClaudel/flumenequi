from datetime import datetime, timedelta
ts = []

with open("log_3servers") as f:
    for line in f:
        if "sleep 5m" in line:
            ts.append(datetime.strptime(line.split(" ")[0].split("+")[-1], "%H:%M:%S"))
res = []
for i in range(len(ts) - 1):
    d = (ts[i + 1] - ts[i]).total_seconds()
    if d < 0:
        d += timedelta(days=1).total_seconds()
    res.append(d)
print(res)
