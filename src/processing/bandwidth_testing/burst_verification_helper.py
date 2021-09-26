import numpy as np
from tqdm import tqdm

def hist_approach(f_time, filter_width, num_pkts, data_lens, times, bursts):

    #number of boundaries that exist
    num_boundaries =  int(f_time // filter_width)
    #space between boundaries is therefore
    bound_index = int(num_pkts // num_boundaries)

    #debug
    #print(num_pkts)
    #print(f_time)
    print('Verify this is sufficient for a meaningful average: {}'.format(bound_index))

    ave_data = []
    init_time = []

    ave_burst = []

    for i in tqdm(range(0,num_pkts,bound_index)):
        init_time.append(times[i])
        ave_data.append(sum(data_lens[i:i+bound_index]))
        ave_burst.append(sum(bursts[i:i+bound_index]))


    ave_data = np.divide(ave_data,125e6) #x8/1e9 to get Gb

    ave_data = np.divide(ave_data, filter_width*1e-6) # to get Gbps

    #print(ave_burst,np.max(ave_burst))
    return init_time, ave_data, ave_burst

def mv_ave_approach(filter_depth, num_pkts, data_lens, times, bursts):
    #default step size is half the filter depth (rounded up)
    steps = int(filter_depth // 2) + 1

    time_list = []
    ave_bw = []
    ave_burst = []

    filter_depth = int(filter_depth)
    num_pkts = int(num_pkts)
    if num_pkts < filter_depth:
        print("Insufficent packets for filter depth, are you sure you are in right mode?")
        exit()


    for i in tqdm(range(0,num_pkts-filter_depth,steps)):
        time_elapsed = (times[i+filter_depth] - times[i]) * 1e-6 #in sec
        if time_elapsed == 0:
            time_elapsed = (times[i+filter_depth+1] - times[i]) * 1e-6 #in sec
        bw_est = sum(data_lens[i:i+filter_depth]) / time_elapsed #in Bps
        bw_est = bw_est * 8 / 1e9
        time_anchor = times[i+filter_depth//2]
        burst_detect = sum(bursts[i:i+filter_depth])

        time_list.append(time_anchor)
        ave_bw.append(bw_est)
        ave_burst.append(burst_detect)




    return time_list, ave_bw, ave_burst