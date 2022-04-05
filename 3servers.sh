#!/usr/bin/env bash
set -x
PS4='+\t '
let dir="$1+30"
cd src/network/
ulimit -n 24096
./multi_server.sh &> server_log &
cd ../..
for load in 1 5 10 15 20 24; do
	for batch_size in {16..256..48}; do
		./get_nccl_ports.sh traffic_logs/"$load"G-3-"$batch_size" &
		timeout "$1"s mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot --mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H liangyu:1,kasra:1,juno:1 -x NCCL_IB_DISABLE=1 -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV -v python src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 --epochs 1 -p 1 -b $batch_size > test_logs/"$load"G-3-"$batch_size" &
		sleep 19s
		sleep "$dir"s
	       	sleep 1m
	done;
done;
for batch_size in {16..256..48}; do
	./get_nccl_ports.sh traffic_logs/0G-3-"$batch_size" &
	timeout "$1"s mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot --mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H liangyu:1,kasra:1,juno:1 -x NCCL_IB_DISABLE=1 -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV -v python src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 --epochs 1 -p 1 -b $batch_size > test_logs/0G-3-"$batch_size"
	sleep 1m
done;
cd traffic_logs
for b in {16..256..48}; do for rate in 0 1 5 10 15 20 24; do python compute_rate.py "$rate"G-3-$b 0 >> "recap-3-ml-`date +%m-%d-%Y`"; done; done
