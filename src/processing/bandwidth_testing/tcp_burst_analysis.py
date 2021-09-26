# TCP Burst Analysis
# What's going on on the link when we're driving it with burst analysis only

import numpy as np
import argparse

from burst_verification_helper import mv_ave_approach

parser = argparse.ArgumentParser(description='Process TCPdump for bandwidth analysis')
parser.add_argument('inputfile_name',
                    help='filename')
parser.add_argument('savefile_name',
                    help='Where should I save csv?')
parser.add_argument('us_width',
                    help='width to set filter at')

args = parser.parse_args()


fp = open(args.inputfile_name, 'r')
count = 0
dbls = 0

filter_width = float(args.us_width) * 1e-6 #in seconds

filter_depth = int(args.us_width)

times = []
data_lens = []

while True:
    

    line = fp.readline()

    if not line:
        break

    line = line.split(' ')
    if len(line) <2:
        continue

    count += 1
    pkt_time = line[0].split(":")
    secs = float(pkt_time[2])
    mins = float(pkt_time[1])
    hrs = float(pkt_time[0])

    #find packet length:
    pkt_length = line[-1]
    pkt_length = int(pkt_length)

    if(count==1):
        times.append(0.)
        total_time = 0
        data_lens.append(pkt_length)
    else:
        elapsed_secs = secs-old_secs
        elapsed_mins = mins-old_mins
        elapsed_hrs = hrs-old_hrs
        elapsed_time = elapsed_secs + elapsed_mins*60 +elapsed_hrs*3600
        total_time = elapsed_time + times[-1]
        #print("total time {}; old_total {}".format(total_time,old_total) )
        if (old_total == total_time):
            dbls += 1
            #print("double up number {}".format(dbls))
            #add the new packets to the last time's entry, don't add the time
            data_lens[-1] += pkt_length
        else:
            #some time has elapsed, so add new point to both lists
            times.append(total_time)
            data_lens.append(pkt_length)

    old_total = total_time
    old_secs = secs
    old_mins = mins
    old_hrs = hrs

print("number of double ups total:{}".format(dbls))
    
    
fp.close()

#----------
#processing
#----------
num_pkts = len(data_lens)

thresh = 25 # for custom bursts using the 400+exponential distribution threshold

print('Threshold is: {}'.format(thresh))

time_int = np.multiply(np.diff(times),1e6)

indicies = np.asarray(time_int < thresh).nonzero()

long_term_ave = sum(data_lens) / (times[-1] * 125e6)

if not indicies:
    print("No burst indicies found")
    exit()

bursts = np.zeros(num_pkts)
for i in indicies: 
    bursts[i] = 1

times = np.multiply(times,1e6)

time_list, ave_bw, ave_burst = mv_ave_approach(filter_depth, num_pkts, data_lens, times, bursts)

time_list = np.multiply(time_list, 1e-6)

ave_burst = np.divide(ave_burst,np.max(ave_burst))


print(long_term_ave)


num_entries = len(ave_bw)

with open(args.savefile_name, 'w') as fp2:
    for i in range(num_entries):
        fp2.write("{}, {}, {}\n".format(
            time_list[i],ave_bw[i],ave_burst[i])
        )

    fp2.close()