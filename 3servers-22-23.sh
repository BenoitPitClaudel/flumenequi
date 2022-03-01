#!/usr/bin/env bash
set -x
PS4='+\t '
let dir="$1+30"
cd src/network/
ulimit -n 24096
./multi_server.sh &> server_log &
cd ../..
for load in 22 23; do
	for batch_size in {16..256..48}; do
		./get_nccl_ports.sh traffic_logs/"$load"G-3-"$batch_size" &
		timeout "$1"s mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot --mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H liangyu:1,kasra:1,juno:1 -x NCCL_IB_DISABLE=1 -x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV -v python src/distributed_learning/pytorch_imagenet.py --synth -a resnet50 --epochs 1 -p 1 -b $batch_size > test_logs/"$load"G-3-"$batch_size" &
		cd src/network/
		sleep 19s
		./client < configs/$dir/"$load"G_consist_to_"$2".config &> client_log_"$2" &
		mkdir -p bws
		cd ../..
		sleep "$dir"s
	       	sleep 5m
		mv src/network/bw.txt src/network/bws/"$load"G-3-"$batch_size"
	done;
done;
cd traffic_logs
for b in {16..256..48}; do for rate in 22 23; do python compute_rate.py "$rate"G-3-$b 0 >> "recap-3-ml-`date +%m-%d-%Y`"; done; done
cd ../src/network
for b in {16..256..48}; do for rate in 22 23; do python read_bw.py bws/"$rate"G-3-$b 0 >> "recap-3-bg-`date +%m-%d-%Y`"; done; done
