# Config Burst Analysis
# What're we asking to be on the link when I run with burst mode?

import numpy as np
import argparse
from burst_verification_helper import hist_approach, mv_ave_approach

parser = argparse.ArgumentParser(description='Process a load config file for analysis')
parser.add_argument('inputfile_name',
                    help='filename')
parser.add_argument('savefile_name',
                    help='Where should I save csv?')
parser.add_argument('us_width',
                    help='width to set filter at')

args = parser.parse_args()

fp = open(args.inputfile_name, 'r')
count = 0

filter_width = float(args.us_width) #in useconds

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

    times.append(int(line[0]))
    data_lens.append(int(line[1]))
    
fp.close()

#----------
#processing
#----------

num_pkts = len(data_lens)

c_time = 0
f_time = times[-1]

time_int = np.diff(times)

#print(time_int)

ave_int = np.mean(time_int)
sd_int = np.std(time_int)

thresh = 800 # for custom bursts using the 400+exponential distribution threshold

print('Threshold is: {}'.format(thresh))

indicies = np.asarray(time_int < thresh).nonzero()


if not indicies:
    print("No burst indicies found")
    exit()

bursts = np.zeros(num_pkts)
for i in indicies: 
    bursts[i] = 1


#-----
#run the averaging algorithm:
#-----
long_term_ave = sum(data_lens) / (times[-1]) * 8e-3

print('Long term average is: {}'.format(long_term_ave))

#histogram like binning
#init_time, ave_data, ave_burst = hist_approach(f_time, filter_width, num_pkts, data_lens, times, bursts)

#moving average style approach
init_time, ave_data, ave_burst = mv_ave_approach(filter_width, num_pkts, data_lens, times, bursts)

ave_burst = np.divide(ave_burst,np.max(ave_burst))

init_time = np.divide(init_time,1e6)

num_entries = len(ave_data)

with open(args.savefile_name, 'w') as fp2:
    for i in range(num_entries):
        fp2.write("{}, {}, {}\n".format(
            init_time[i],ave_data[i],ave_burst[i])
        )

    fp2.close()