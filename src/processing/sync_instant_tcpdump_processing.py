import numpy as np
import argparse
from tqdm import tqdm

#modified to support averaging to improve SD

parser = argparse.ArgumentParser(description='Process TCPdump logs from three sources, synchronizing packet arrival times with internal clocks')
parser.add_argument('file1',
                    help='filename')
parser.add_argument('file2',
                    help='filename')
parser.add_argument('file3',
                    help='filename')
parser.add_argument('value',
                    help='Nominal Gbps value/index')
parser.add_argument('init_start_point',
                    help='number of values to initially skip')
parser.add_argument('num_samples',
                    help='how many values to sample from file')
parser.add_argument('output_fname',
                    help='output filename')
parser.add_argument('--filter_width', default = 30,
                    help='how many values to average in moving average filter')


def mv_ave_approach(filter_depth, num_pkts, data_lens, times):
    #default step size is half the filter depth (rounded up)
    steps = int(filter_depth // 2) + 1

    time_list = []
    ave_bw = []

    filter_depth = int(filter_depth)
    num_pkts = int(num_pkts)
    if num_pkts < filter_depth:
        print("Insufficent packets for filter depth, are you sure you are in right mode?")
        exit()

    for i in tqdm(range(0,num_pkts-filter_depth,steps)):
        time_elapsed = (times[i+filter_depth] - times[i]) #in sec
        if time_elapsed == 0:
            time_elapsed = (times[i+filter_depth+1] - times[i]) #in sec
        bw_est = sum(data_lens[i:i+filter_depth]) / time_elapsed #in Bps
        bw_est = bw_est * 8 / 1e9
        time_anchor = times[i+filter_depth//2]

        time_list.append(time_anchor)
        ave_bw.append(bw_est)

    return time_list, ave_bw


def main():

    args = parser.parse_args()

    entry = args.value
    start = int(args.init_start_point)
    num_samples = int(args.num_samples)

    filter_width = int(args.filter_width)

    fp1 = open(args.file1, 'r')
    fp2 = open(args.file2, 'r')
    fp3 = open(args.file3, 'r')

    
    dbls = 0

    start_count = 0

    print('Load in Data')
    
    times1 = []
    data_lens1 = []
    times2 = []
    data_lens2 = []
    times3 = []
    data_lens3 = []
    data_total = np.zeros((3,1))
    startup=1
    actual_start = int(start)

    secs = np.zeros((3,1))
    old_secs = np.zeros((3,1))
    mins = np.zeros((3,1))
    old_mins = np.zeros((3,1))
    hrs = np.zeros((3,1))
    old_hrs = np.zeros((3,1))

    #print(times)
    #print(data_lens)
    #print(data_total)

    #initialization loop
    print('Initialising')
    while True:
    #for i in tqdm(range(actual_start, actual_start+num_samples, 1)):


        line1 = fp1.readline()
        line2 = fp2.readline()
        line3 = fp3.readline()


        # line counter
        start_count += 1

        if not line1:
            print('End of File 1')
            break
        if not line2:
            print('End of File 2')
            break
        if not line3:
            print('End of File 3')
            break

        #delay to start
        if actual_start-1 > start_count:
            continue

        
        
        line1 = line1.split(' ')
        line2 = line2.split(' ')
        line3 = line3.split(' ')
        if len(line1) < 2 or len(line2) < 2 or len(line3) < 2:
            print('invalid line: {} {} {}'.format(len(line1),len(line2),len(line3)))
            continue

        payload_len1 = line1[-1]
        payload_len1 = int(payload_len1)
        payload_len2 = line2[-1]
        payload_len2 = int(payload_len2)
        payload_len3 = line3[-1]
        payload_len3 = int(payload_len3)

        data_total[0] += payload_len1
        data_total[1] += payload_len2
        data_total[2] += payload_len3

        # time = datetime.datetime.strptime(time[0], "%H:%M:%S.%f")
        for i in range(3):
            if i == 1:
                pkt_time = line1[0].split(":")
            elif i == 2:
                pkt_time = line2[0].split(":")
            else:
                pkt_time = line3[0].split(":")
            secs[i] = float(pkt_time[2])
            mins[i] = float(pkt_time[1])
            hrs[i] = float(pkt_time[0])

        if(startup == 1):
            tol = 1e-5
            init_time = secs + mins*60 + hrs*3600

            min_time = np.min(init_time)

            for k in range(3):
                if init_time[k] <= min_time+tol :
                    min_ind = k

            min_ind = np.where(init_time == np.amin(init_time))
            #store as the initial time an offset based on the global minimum time found
            times1.append(init_time[0]-init_time[min_ind])
            times2.append(init_time[1]-init_time[min_ind])
            times3.append(init_time[2]-init_time[min_ind])

            data_lens1.append(payload_len1)
            data_lens2.append(payload_len2)
            data_lens3.append(payload_len3)
            startup = 0
            #finish the start up by specifying the old times
            old_secs = np.copy(secs)
            old_mins = np.copy(mins)
            old_hrs = np.copy(hrs)
            break

    print("Running through Each File")
    for i in range(3):
        #process whole of file, one at a time:
        count = start_count

        if i == 0:
            old_total = times1[0]
        elif i == 1:
            old_total = times2[0]
        else: 
            old_total = times3[0]
        

        while True:
            if i == 0:
                line = fp1.readline()
            elif i == 1:
                line = fp2.readline()
            else: 
                line = fp3.readline()

            if not line:
                print('End of File')
                break

            count += 1

            #exit when done
            if count > actual_start-1+num_samples:
                break
            
            line = line.split(' ')
            if len(line) < 2:
                print('invalid line')
                continue

            payload_len = line[-1]
            payload_len = int(payload_len)

            if payload_len == 0:
                #no data recieved (beyond header - 7 bytes), most likely an ack
                continue

            data_total[i] += payload_len


            # time = datetime.datetime.strptime(time[0], "%H:%M:%S.%f")
            pkt_time = line[0].split(":")
            secs[i] = float(pkt_time[2])
            mins[i] = float(pkt_time[1])
            hrs[i] = float(pkt_time[0])

            #print(secs[i],old_secs[i])

            elapsed_secs = secs[i]-old_secs[i]
            elapsed_mins = mins[i]-old_mins[i]
            elapsed_hrs = hrs[i]-old_hrs[i]
            elapsed_time = elapsed_secs + elapsed_mins*60 + elapsed_hrs*3600
            #increase total time by whichever elapsed time is counting from 0
            if i == 0:
                total_time = elapsed_time + times1[-1]
            elif i == 1:
                total_time = elapsed_time + times2[-1]
            else: 
                total_time = elapsed_time + times3[-1]
            # print("total time {}; old_total {}".format(total_time,old_total) )
            if (old_total == total_time):
                dbls += 1
                    # print("double up number {}".format(dbls))
                    # add the new packets to the last time's entry, don't add the time
                if i == 0:
                    data_lens1[-1] += payload_len
                elif i == 1:
                    data_lens2[-1] += payload_len
                else: 
                    data_lens3[-1] += payload_len   
            else:
                # some time has elapsed, so add new point to both lists
                if i == 0:
                    times1.append(total_time)
                    data_lens1.append(payload_len)
                elif i == 1:
                    times2.append(total_time)
                    data_lens2.append(payload_len)
                else: 
                    times3.append(total_time)
                    data_lens3.append(payload_len)

            old_total = total_time
            old_secs = np.copy(secs)
            old_mins = np.copy(mins)
            old_hrs = np.copy(hrs)

        print("Completed File {}".format(i+1))
            
    fp1.close()
    fp2.close()
    fp3.close()

    print("Processing")

    if(min_ind == 0):
        time_tot = times1[-1]
    elif(min_ind == 1):
        time_tot = times2[-1]
    else:
        time_tot = times3[-1]

    long_term_ave = np.zeros((3,1))

    long_term_ave[0] = data_total[0] / (times1[-1] * 125e6)
    long_term_ave[1] = data_total[1] / (times2[-1] * 125e6)
    long_term_ave[2] = data_total[2] / (times3[-1] * 125e6)

    filter_depth = filter_width

    num_pkts = np.zeros((3,1))

    num_pkts[0] = len(times1)
    num_pkts[1] = len(times2)
    num_pkts[2] = len(times3)

    time_list1, ave_bw1= mv_ave_approach(filter_depth, num_pkts[0], data_lens1, times1)
    time_list2, ave_bw2 = mv_ave_approach(filter_depth, num_pkts[1], data_lens2, times2)
    time_list3, ave_bw3 = mv_ave_approach(filter_depth, num_pkts[2], data_lens3, times3)

    varBW1 = np.std(ave_bw1)
    varBW2 = np.std(ave_bw2)
    varBW3 = np.std(ave_bw3)


    # output to write for CLI
    print("Speed: {}, Total Time Processed: {}".format(entry,time_tot))
    print("Input 1, Input 2, Input 3")
    print("{}, {}, {}".format(long_term_ave[0],long_term_ave[1],long_term_ave[2]))
    print("{}, {}, {}".format(varBW1,varBW2,varBW3))

    filename = [args.output_fname + "_1.csv", args.output_fname + "_2.csv", args.output_fname + "_3.csv"]
    

    for y in range(3):
        if y == 0:
            time_list = time_list1
            ave_bw = ave_bw1
        elif y == 1:
            time_list = time_list2
            ave_bw = ave_bw2
        else: 
            time_list = time_list3
            ave_bw = ave_bw3

        num_entries = len(time_list)

        with open(filename[y], 'w') as fpout:
            for x in range(num_entries):
                fpout.write("{}, {}\n".format(
                    float(time_list[x]),float(ave_bw[x]))
                )

            fpout.close()
      

if __name__ == "__main__":
    main()
