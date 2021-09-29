#!/bin/bash

ulimit -n 24096

#set the appropriate interface for the experiment at the -i flag:
sudo tcpdump -i enp194s0 -Q out -l > ~/webs_logs/tcp_consistent_resnet_10G.txt &
#note need sudo for tcpdump here

#do not run this task in background unless calling directly on client server terminal
../src/network/client < ../src/network/load_generation/consistent_loads/10G.config

#client_run filled with example parameters for a 10G Websearch load, 
#generated from load_generation tools and stored in the webs_loads folder