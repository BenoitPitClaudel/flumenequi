#!/bin/bash

source ~/.bashrc

#set the appropriate conda environment
conda activate hvd_21

ulimit -n 24096

#Start Servers - these will likely be running from the first experiment, can omit if running repeated back to back
/path/to/james-flumenequi/src/network/multi_server.sh &
#give TCP servers a moment to initalize
sleep 1

#call client_run script on client server, in this case cowan, need sudo access for tcpdump
ssh <user>@cowan.csail.mit.edu '/path/to/james-flumenequi/run_scripts/client_run.sh' &

#call main machine learning task, can swap models, machines, etc as required, further example commands in readme.md
/usr/local/openmpi-4.1.1/bin/mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot \
--mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 \
--mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H abtin:1,bly:1,dara:1 -x NCCL_IB_DISABLE=1 \
-x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV \
python ~/path/to/james-flumenequi/src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 \
--epochs 1 -p 1 -b 64 > ~/consistent_logs/iter_consistent_resnet_10G.txt &
#modify the log location in the final line to match that in client_run.sh, with iter prefix for iteration