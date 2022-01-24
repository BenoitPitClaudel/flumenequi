import numpy as np
with open("bw.txt") as f:
    ln = 0
    bws = []
    for line in f:
        ln += 1
        if ln <= 3:
            continue
        if ln >= 80:
            break
        bws.append(float(line.split(" ")[0]))
avg = np.mean(bws)
removed = 0
bws.pop()
while len(bws) > 0:
    last = bws.pop()
    if last > avg/4:
        bws.append(last)
        break
    else:
        removed += 1
print("mean: {}, std: {}, removed {} at the end".format(np.mean(bws), np.std(bws), removed))
