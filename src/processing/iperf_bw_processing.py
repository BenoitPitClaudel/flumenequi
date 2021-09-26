import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Process BW sample logs from iperf utility')
parser.add_argument('file',
                    help='filename')
parser.add_argument('value',
                    help='Nominal Gbps value')
parser.add_argument('-num_ports')

args = parser.parse_args()

entry=args.value

ports=int(args.num_ports)

fp = open(args.file, 'r')
count = 0

bws = []

while True:

    line = fp.readline()

    if not line:
        break

    if (ports!=1):
        line = line.split('SUM]')
        if len(line) <2:
            continue
        line = line[1]

    line = line.split('Mbits/sec')
    if len(line) <2:
        continue

    line = line[0].split('Bytes')
    
    #line = line[1].split('(')
    #select current not running average value
    count += 1
    bw = float(line[1].strip())

    if (count == 1):
        continue #trim first entry
    else:
        bws.append(bw)

bw_measured = np.asarray(bws)

ave = np.mean(bw_measured)
sig = np.std(bw_measured)

sorted = np.sort(bw_measured)

size = sorted.shape

#tail_ind = int(np.ceil(size[0]*tail_percent))

#print("Mean: {}, std: {}".format(ave,sig))

print("{},{},{}".format(entry,ave,sig))


#print("Tail99: {}".format(sorted[tail_ind]))
 
fp.close()