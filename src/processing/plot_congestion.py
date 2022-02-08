import argparse
import numpy as np
import re
import os
from collections import defaultdict, namedtuple
import matplotlib.pyplot as plt

filenames_regex = re.compile('.*?(?P<bw>[0-9]+)G-(?P<nodes>[0-9]+)-(?P<batch_size>[0-9]+)')
lines_regex = re.compile('\[[0-9],(?P<rank>[0-9])\][a-zA-Z<>:/0-9\]\[\s]*?Time\s+(?P<time>[0-9\.]+)\s+\([0-9 \.]+\)')

parser = argparse.ArgumentParser(description="Iteration time parser and plotter")
parser.add_argument('-d', '--directory', help="Log files directory", type=str)
parser.add_argument('-b', '--bandwidths', help="List of background traffic BW", type=int, nargs='+')
parser.add_argument('-et', '--end-truncate', help="How many values to truncate from the end of the run", type=int)
parser.add_argument('-st', '--start-truncate', help="How many values to truncate from the beginning of the run", type=int)
parser.add_argument('-n', '--nodes', help="How many nodes to consider for processing", type=int)
args = parser.parse_args()
data = {bw: defaultdict(list) for bw in args.bandwidths}
for filename in os.listdir(args.directory):
    f = os.path.join(args.directory, filename)
    if os.path.isfile(f):
        m = filenames_regex.match(f)
        if not m or int(m.group("bw")) not in args.bandwidths or int(m.group("nodes")) != args.nodes:
            continue
        with open(f, "r") as fh:
            for line in fh:
                ml = lines_regex.match(line)
                if ml:
                    data[int(m.group("bw"))][int(m.group("batch_size"))].append(float(ml.group("time")))
Stats = namedtuple("Stats", "batch_size avg std")
def mk_stats(size, b):
    return Stats(size, np.mean(b), np.std(b))
stats = {k: [mk_stats(size, b) for size, b in sorted(batches.items())]
         for k, batches in data.items()}
for k, sts in stats.items():
    batch_sizes, avgs, stds = zip(*sts)
    plt.errorbar(batch_sizes, avgs, yerr=stds, label="{}Gbps".format(k), capsize=4)
plt.legend()
plt.tight_layout()
plt.savefig("temp.pdf")
plt.close()
