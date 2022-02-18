import numpy as np
import sys
try:
    with open(sys.argv[1]) as f:
        ln = 0
        bws = []
        for line in f:
            ln += 1
            if ln <= 3:
                continue
            #if ln >= 80:
             #   break
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
    print("XP:{}, mean: {}, std: {}, removed {} at the end".format(sys.argv[1], np.mean(bws), np.std(bws), removed))
except FileNotFoundError:
    print("XP:{}, mean: 0, std: 0, removed 0 at the end".format(sys.argv[1]))
