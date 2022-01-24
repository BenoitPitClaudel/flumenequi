#!/usr/bin/env bash
set -x
PS4='+\t '
let dir="$1+30"
let log_time="$1-100"
cd src/network/
ulimit -n 24096
./multi_server.sh &> server_log &
cd ../..
for batch_size in {16..256..48}; do
	timeout "$log_time"s tcpdump -i enp194s0 -Q out -l > traffic_logs/0G-4-"$batch_size" &
	timeout "$1"s mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot --mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 4 -H iraj:1,liangyu:1,kasra:1,juno:1 -x NCCL_IB_DISABLE=1 -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV -v python src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 --epochs 1 -p 1 -b $batch_size > test_logs/0G-4-"$batch_size"
	sleep 5m
done;
for load in 10 20; do
	for batch_size in {16..256..48}; do
		cd src/network/
		./client < configs/$dir/"$load"G_consist_to_"$2".config &> client_log_"$2" &
		pidc=$!
		cd ../..
		timeout "$log_time"s tcpdump -i enp194s0 -Q out -l > traffic_logs/"$load"G-4-"$batch_size" &
		pidl=$!
		timeout "$1"s mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot --mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 4 -H iraj:1,liangyu:1,kasra:1,juno:1 -x NCCL_IB_DISABLE=1 -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV -v python src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 --epochs 1 -p 1 -b $batch_size > test_logs/"$load"G-4-"$batch_size";
		sleep 1m
		kill $pidc $pidl
		sleep 4m
	done;
done;
