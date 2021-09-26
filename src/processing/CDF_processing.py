import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Process Pytorch Iteration Logs to CDF')
parser.add_argument('inputfile_name',
                    help='filename')
parser.add_argument('savefile_name',
                    help='Where should I save the CDF?')
parser.add_argument('init_trunc',
                    help='How many values to truncate from start of run')
parser.add_argument('trunc',
                    help='How many values to truncate from end of run')
parser.add_argument('--second_input', default = None,
                    help='optional second input file')

args = parser.parse_args()


fp = open(args.inputfile_name, 'r')
count = 0

files = 1

if args.second_input:
    fp2 = open(args.second_input, 'r')
    files = 2


tail_percent = 0.99

times = []

#for each file you need to read
for i in range(files):
    #read a file
    while True:
        
        if i==0:
            line = fp.readline()
        else:
            line = fp2.readline()

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
        
        #if(count % 2 == 0):
        #    print(time)
        #    print(count)
    print("done w one")
    init_trunc = int(args.init_trunc)
    fin_trunc = int(args.trunc)

    if i==0:
        times = times[:-fin_trunc]
        times = times[init_trunc:]
        file1_len=len(times)
    else:
        #remove halfway through file
        times = times[:-fin_trunc]
        for i in range(init_trunc):
            del times[i+file1_len]
    print("first entries:")
    print(times[0:9])
    print("final entires:")
    print(times[-10:])

    #times = times[:-3]

#close open files
fp.close()
if args.second_input:
    fp2.close()


iter_times = np.asarray(times)

sorted_times = np.sort(iter_times)

num_entries = len(sorted_times)


y_cdf = 1. * np.arange(num_entries) / (num_entries-1)


with open(args.savefile_name, 'w') as fpout:
    for i in range(num_entries):
        fpout.write("{}, {}\n".format(
            sorted_times[i],y_cdf[i])
        )

    fpout.close()
 
