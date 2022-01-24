#!/bin/bash
. "/home/benoit/anaconda3/etc/profile.d/conda.sh"
export ENV_PREFIX=$PWD/env
export HOROVOD_CUDA_HOME=$CUDA_HOME
export HOROVOD_NCCL_HOME=$ENV_PREFIX
export HOROVOD_GPU_OPERATIONS=NCCL
eval `ssh-agent`
ssh-add ~/.ssh/mpi_benoit
conda activate /home/benoit/pollux/flumenequi/env
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.0/extras/CUPTI/lib64:/usr/local/bin/mpirun:/usr/local/cuda-11.0/lib64
export PATH=$PATH:$LD_LIBRARY_PATH
sudo setcap cap_net_raw+ep "$(command -v iftop)"
sudo setcap cap_net_raw+ep "$(command -v tcpdump)"
