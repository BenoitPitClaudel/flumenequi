import numpy as np
import random
import argparse

from helper import write_output, burst_gen_v4, burst_gen_v5

# modified to verify correct burst operation

parser = argparse.ArgumentParser(description='Generate Burst Web-Search Traffic')
parser.add_argument('gbps',
                    help='target load to achieve in Gbps')
parser.add_argument('duration',
                    help='length of file in seconds')
parser.add_argument('--burst_width', default=1000,
                    help='define burst width profile in us - default 1000')
parser.add_argument('--destination', default = 0,
                    help='set the destination index - default 0')  

# load distribution from file:

def main(target_load, destination, burst_width, duration, filename):
    burst_height = 3
    #-------------------------------
    #fixed regardless of burst_width
    #-------------------------------

    #default value for sufficient points cases
    scaling = 1
    #design capacity - 25Gbps - capacity = total data capacity in bytes
    capacity = 25 * duration * 1e9 / 8 
    
    #pre-calculated average size from the distribution
    ave_data = 1622.94
    #convert to bytes
    ave_data = np.multiply(ave_data, 1460)
    #duration converted to us, normal is in s
    duration_us = duration * 1e6

    #-------------------------------
    #modified by burst_width
    #-------------------------------

    #duration of burst is given by burst_width
    burst_duration = burst_width
    burst_off_duration = burst_width * 9 #total 10x burst width
    #number of bursts in full sample
    num_bursts = int(duration_us // (10*burst_width))
    #print(num_bursts)
    
    #req data to be generated - total
    data_req = target_load * duration * 1e9 / 8 #in bytes

    #req data per burst pattern
    data_req_burst_pat = data_req / num_bursts
    #split data required into burst/no burst sections: non-burst is what's left over
    #burst_height of 1 is it's fair share
    burst_data = data_req_burst_pat / 10 * burst_height
    non_burst_data = data_req_burst_pat - burst_data

    #print(data_req_burst_pat)
    #print(burst_data)
    #print(non_burst_data)
    #print(ave_data)
    
    #flow_times, size_bytes = burst_gen_v4(burst_data,non_burst_data,ave_data,burst_duration,burst_off_duration,num_bursts)
    flow_times, size_bytes = burst_gen_v5(burst_data,non_burst_data,ave_data,burst_duration,burst_off_duration,num_bursts)

    cum_sum_times = np.cumsum(flow_times)

    #output section
    write_output(filename, destination, size_bytes, cum_sum_times)
    # write_output(filename, size_bytes, flow_times)
    # print(size_bytes.shape)


if __name__ == "__main__":

    args = parser.parse_args()
    # in Gbps
    target_load = float(args.gbps)
    burst_width = float(args.burst_width)
    # in seconds
    duration = float(args.duration)

    destination = str(args.destination)

    filename = args.gbps + "G_burst.config"
 
    main(target_load, destination, burst_width, duration, filename)
