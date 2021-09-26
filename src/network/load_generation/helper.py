import numpy as np
import random
import os

def burst_gen_v5(burst_data,non_burst_data,ave_data,burst_duration,burst_off_duration,num_bursts):
    #default scaling
    scaling = 1
    
    height_split, spacing, start = randomise_burst(burst_duration,num_bursts)

    #noburst is the same as v4, except floored
    samples_nbrs = int(np.floor(non_burst_data / ave_data))

    if(samples_nbrs<8):
        print("Number of NoBurst Samples is only: {}. Modifying to force 8 ".format(samples_nbrs))
        samples_nbrs = 8
        #force sample number to minimum, recalc ave_data
        ave_data_mod = non_burst_data / samples_nbrs
        #print(ave_data_mod)
        #recalc samples_no burst, calc scaling factor
        samples_nbrs = int(np.floor(non_burst_data / ave_data_mod))
        #print(samples_nbrs)
        scaling = ave_data_mod / ave_data 
        #now we have scaling factor, overwrite average data with updated value

    param_nbrs = burst_off_duration / samples_nbrs

    weighted_size = load_distribution(scaling)

    flow_times = []
    size_bytes = []
    for i in range(num_bursts):
        times_brst = [start[i], start[i] + spacing[i]]
        size_brst = [burst_data * height_split[i], burst_data * (1-height_split[i])]
        times_nbrs,size_nbrs = sample_section(param_nbrs,samples_nbrs,weighted_size)

        flow_times.extend(times_brst)
        flow_times.extend(times_nbrs.tolist())
        size_bytes.extend(size_brst)
        size_bytes.extend(size_nbrs.tolist())

    return flow_times, size_bytes

def burst_gen_v4(burst_data,non_burst_data,ave_data,burst_duration,burst_off_duration,num_bursts): 
    #default if not changed
    scaling = 1
    #number of samples required per burst pattern
    samples_brst = int(np.floor(burst_data / ave_data))
    samples_nbrs = int(np.floor(non_burst_data / ave_data))

    if(samples_brst<9):
        print("Number of Burst Samples is only: {}. Modifying to force 8 ".format(samples_brst))
        samples_brst = 8
        #force sample number to minimum, recalc ave_data
        ave_data_mod = burst_data / samples_brst
        #print(ave_data_mod)
        #recalc samples_no burst, calc scaling factor
        samples_nbrs = int(np.floor(non_burst_data / ave_data_mod))
        #print(samples_nbrs)
        if(samples_nbrs<9):
            print("Caution Samples NoBurst is: {} CHECK".format(samples_nbrs))
        scaling = ave_data_mod / ave_data 
        #now we have scaling factor, overwrite average data with updated value
        ave_data = ave_data_mod

    #rescale weighted size if required (defaults to 1 if not)
    weighted_size = load_distribution(scaling)

    #print(samples_nbrs)
    #print(samples_brst)

    
    #poisson parameter is:
    param_brst = burst_duration / samples_brst
    param_nbrs = burst_off_duration / samples_nbrs

    #print(param_brst)
    #print(param_nbrs)

    flow_times = []
    size_bytes = []
    for i in range(num_bursts):
        times_brst,size_brst = sample_section(param_brst,samples_brst,weighted_size)
        times_nbrs,size_nbrs = sample_section(param_nbrs,samples_nbrs,weighted_size)

        flow_times.extend(times_brst.tolist())
        flow_times.extend(times_nbrs.tolist())
        size_bytes.extend(size_brst.tolist())
        size_bytes.extend(size_nbrs.tolist())

    return flow_times, size_bytes

def randomise_burst(burst_duration,num_bursts):
    #burst, we are making 2 and only two points, for which we need 3 random numbers:
    height = np.random.normal(0.5,0.08,num_bursts)
    spacing = np.random.exponential(200,num_bursts)+300
    start = np.random.uniform(0,burst_duration - spacing,num_bursts)
    return height,spacing,start

def sample_section(param,samples,weighted_size):

    flow_times = np.random.poisson(param,samples)

    #cum_sum_times = np.cumsum(flow_times)
    
    samples = len(flow_times)

    size = random.choices(weighted_size[0,:],cum_weights=weighted_size[1,:],k=samples)

    size_bytes = np.multiply(size,1460)

    return flow_times, size_bytes


#unmodified

def write_output(filename, destination, size_bytes, times):
    fp = open(filename,'w')


    num_flows = len(size_bytes)
    #+" "+str(num_repeats)+"\n")
    fp.write(str(num_flows)+"\n")
    for i in range(num_flows):
        fp.write(str(int(times[i]))+" "+str(int(size_bytes[i]))+" "+destination+"\n")

    fp.close()

def load_distribution(scaling):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    fp = open(os.path.join(__location__, "CDF_search.tcl"),'r')

    cdf = []
    value = []

    while True:
        line = fp.readline()
        if not line:
            break

        line = line.split(' ')
        value.append(float(line[0]))
        cdf.append(float(line[2]))

    fp.close()

    weighted_size = np.asarray((value,cdf))

    weighted_size[0,:] = np.multiply(weighted_size[0,:],scaling)

    return weighted_size
