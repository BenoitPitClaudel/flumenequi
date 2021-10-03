# TCP Load Generation Code

Acknowledgement: The multithreaded TCP client/server code was developed with Sudarsanan Rajasekaran. Thank you greatly for your help!

## Setup:

1. Set required IP addresses in [tcp_load_clientside](tcp_load_clientside.cpp) from lines 72-90, this code assumes up to a maximum of 4 destinations, if more are required, modify this if statement.

2. Set number of parallel helper threads using the 'num_helper_threads' parameter on line 22. I have found that 3 is a good number for up to 25 Gbps of traffic.

3. If required, change the default TCP destination port used from 818080. This is defined on line 173 in [tcp_load_clientside](tcp_load_clientside.cpp).

3. Build with the makefile.

4. Add run permissions with 'chmod +x client server'

Code is configured for up to 5 minute runs, this can be extended by changing the sleep time on the main thread in line 253.

## To Run:

### Source Side:
1. Generate required load using either 'generate_load_burst.py' or 'generate_load_consist.py'
> python generate_load_<burst/consist>.py load duration --destination --burst-width 
2. Increase filelimit using the 'ulimit' command, eg: 'ulimit -n 24096'
3. Call 'client' on the server using the following syntax:
> ./client < /path/to/load_file.config
4. Monitor printouts to ensure logical operation
5. Use ctrl-c to abort/terminate runs if required

### Destination Side
1. Increase file limit using the 'ulimit' command, eg: 'ulimit -n 24096'
2. Either run the following bash script on the destination server;
> ./multi-server.sh
or manually call 'server' the number of times specified by 'num_helper_threads' using the following syntax, iterating the final number as appropriate
> ./server 818080 &
> ./server 818081 &
> ./server 81808[n] &
3. Monitor printouts to ensure sockets are closed

## RDMA counter probe
To monitor the Mellanox RDMA packet counters, one can make use of the c++ script provided in [RDMA_counter](RDMA_counter), explained [here](RDMA_counter/readme.md).