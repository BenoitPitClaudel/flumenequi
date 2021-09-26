import numpy as np
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Process TCPdump logs')
parser.add_argument('file',
                    help='filename')
parser.add_argument('value',
                    help='Nominal Gbps value/index')
parser.add_argument('init_start_point',
                    help='number of values to initially skip')
parser.add_argument('filter_length')
parser.add_argument('--all_results',default=False,action='store_true',
                    help='print all results to allow histogram generation')


def main():

    args = parser.parse_args()

    entry = args.value
    start = int(args.init_start_point)
    
    filter_length = int(args.filter_length)

    fp = open(args.file, 'r')
    tail = 0.99

    dbls = 0

    count = 0

    data_total = 0
    startup = True
    actual_start = int(start)

    exitwhile = False

    local_data_list = np.zeros((filter_length,1))
    local_time_list = np.zeros((filter_length,1))

    bw_est = []
    anchor = []

    running_time = 0

    while True:

        data_total = 0

        for i in range(filter_length):
            line = fp.readline()
            # line counter
            count += 1

            if not line:
                print('End of File')
                exitwhile = True
                break

            #delay to start
            if actual_start-1 > count:
                continue

            #exit when done
            #if count > actual_start-1+num_samples:
            #    break
        
            line = line.split(' ')
            if len(line) < 2:
                continue

            payload_len = line[-1]
            payload_len = int(payload_len)

            data_total += payload_len

            # time = datetime.datetime.strptime(time[0], "%H:%M:%S.%f")
            pkt_time = line[0].split(":")
            secs = float(pkt_time[2])
            mins = float(pkt_time[1])
            hrs = float(pkt_time[0])

            if startup == True:
                startup = False
            else:
                elapsed_secs = secs-old_secs
                elapsed_mins = mins-old_mins
                elapsed_hrs = hrs-old_hrs
                elapsed_time = elapsed_secs + elapsed_mins*60 + elapsed_hrs*3600
                local_data_list[i] = payload_len
                local_time_list[i] = elapsed_time
                running_time += elapsed_time

            old_secs = secs
            old_mins = mins
            old_hrs = hrs

            if i == filter_length // 2:
                window_data = np.sum(local_data_list)
                window_time = np.sum(local_time_list)
                if window_time ==0:
                    continue
                bw_est.append( window_data / (window_time * 125e6) ) 
                anchor.append( running_time )
            elif i == filter_length - 1:
                window_data = np.sum(local_data_list)
                window_time = np.sum(local_time_list)
                if window_time ==0:
                    continue
                bw_est.append( window_data / (window_time * 125e6) ) 
                anchor.append( running_time )

        

        if exitwhile:
            break

        
    fp.close()

    num_points = len(bw_est)
       
    BWstdev = np.std(bw_est)

    bw_mean = np.mean(bw_est)

    trunc_bw_est = np.where( bw_est > bw_mean + BWstdev,0, bw_est )
    trunc_bw_est = np.where( bw_est < bw_mean - BWstdev,0, trunc_bw_est )
    
    num_values = np.count_nonzero(trunc_bw_est)

    trunc_bw_mean = sum(trunc_bw_est) / num_values

    # output to write for CLI
    print("{},{},{},{},{},{}".format(entry,bw_mean,trunc_bw_mean,num_points,running_time,BWstdev))

    all_results = args.all_results
    #uncomment to print all results, for histogram processing
    if all_results:
        for j in range(num_points):
            print( "{},{}".format( anchor[j], bw_est[j] ) )


if __name__ == "__main__":
    main()
