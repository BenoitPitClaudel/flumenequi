import numpy as np
import random
import argparse
from helper import load_distribution, write_output



parser = argparse.ArgumentParser(description='Generate Consistent Web-Search Traffic')
parser.add_argument('gbps',
                    help='target load to achieve in Gbps')
parser.add_argument('duration',
                    help='length of output load file in seconds')    
parser.add_argument('--destination', default = 0,
                    help='set the destination index - default 0')        

#load distribution from file:
def main(target_load,destination,duration,filename):

    scaling = 1
    weighted_size = load_distribution(scaling)
    #ave_data = np.average(weighted_size[0,:],weights=weighted_size[1,:])
    ave_data = 1622.94 * scaling
    #print(weighted_size)
    #print(ave_data)
    ave_data = np.multiply(ave_data,1460)
    #print(ave_data)
    #target_load*duration of data -> samples if average data is X
    #param of Y to give that many samples in duration

    #req data
    ave_data = 10E6
    data_req = target_load * duration * 1e9 / 8 #in bytes
    samples = int(np.floor(data_req / ave_data))

    capacity = 25 * duration * 1e9 / 8 

    param = duration * 1e6 / samples


    flow_times = np.random.exponential(param,samples)

    cum_sum_times = np.cumsum(flow_times)

    samples = len(cum_sum_times)
    #size = random.choices(weighted_size[0,:],cum_weights=weighted_size[1,:],k=samples)
    #size = [np.trunc(np.average(weighted_size[0, 1:], weights=(weighted_size[1, 1:] - weighted_size[1, :-1])))] * samples
    #size_bytes = np.multiply(size,1460)
    size_bytes = [ave_data] * samples
    write_output(filename, destination, size_bytes, cum_sum_times)
    #write_output(filename, size_bytes, flow_times)
    #print(size_bytes.shape)

if __name__ == "__main__":

    args = parser.parse_args()
    #in Gbps
    target_load = float(args.gbps)
    #in seconds
    duration = float(args.duration)

    destination = str(args.destination)

    num_repeats = 1

    filename = args.gbps + "G_consist_to_" + str(destination) + ".config"
    main(target_load,destination,duration,filename)
