import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Process Pytorch logs')
parser.add_argument('file',
                    help='filename')
parser.add_argument('value',
                    help='Nominal Gbps value')
parser.add_argument('trunc',
                    help='How many values to truncate from end of run')
parser.add_argument('init_trunc',
                    help='How many values to truncate from start of run')

args = parser.parse_args()

trunc = int(args.trunc)
init_trunc = int(args.init_trunc)

entry=args.value

fp = open(args.file, 'r')
count = 0

tail_percent = 0.99

times = []

while True:
    

    line = fp.readline()

    if not line:
        break

    line = line.split('Time')
    if len(line) <2:
        continue
    count += 1
    line = line[1].split('Data')
    
    line = line[0].split('(')
    #print(line)
    #select current not running average value
    time = float(line[0].strip())
    
    if (count < 4):
        #ignore first 4 entires
        continue
    times.append(time)
    print(time)

iter_times = np.asarray(times)

if trunc != 0:
    iter_times = iter_times[:-trunc]

if init_trunc != 0:
    iter_times = iter_times[init_trunc:]

print("init:")
print(iter_times[0:9])
print("fin:")
print(iter_times[-10:])

ave = np.mean(iter_times)
sig = np.std(iter_times)

num = len(iter_times)

sorted = np.sort(iter_times)

size = sorted.shape

tail_ind = int(np.ceil(size[0]*tail_percent))

if tail_ind == size[0]:
    tail_ind -= 1

print("{},{},{},{},{}".format(entry,ave,num,sig,sorted[tail_ind]))

 
fp.close()
