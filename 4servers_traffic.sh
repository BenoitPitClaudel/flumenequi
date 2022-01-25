#!/usr/bin/env bash
set -x
PS4='+\t '
let log_time="$1-100"
let dir="$1+30"
cd src/network/
ulimit -n 24096
./multi_server.sh &> server_log &
cd ../..
for batch_size in {16..256..48}; do
	./get_nccl_ports.sh traffic_logs/0G-3-"$batch_size" &
	sleep $1
	sleep 5m
done;
for load in 10 20; do
        for batch_size in {16..256..48}; do
		./get_nccl_ports.sh traffic_logs/"$load"G-3-"$batch_size" &
		sleep 19s
		cd src/network/
		./client < configs/$dir/"$load"G_consist_to_"$2".config &> client_log_"$2" &
                cd ../..
		sleep "$dir"s
		sleep 5m
		mv src/network/bw.txt src/network/"$load"G-3-"$batch_size"
		sleep 3s
        done;
done;
cd traffic_logs
for b in {16..256..48}; do for rate in 0 10 20; do python compute_rate.py "$rate"G-3-$b 0 >> "recap-3-ml-`date +%m-%d-%Y`"; done; done
