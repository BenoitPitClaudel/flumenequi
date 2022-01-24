#!/bin/bash
set -x
sleep 10s
tcpdump -c 5000 -i enp194s0 -Q out -l > nccl_ports
ports=(`python get_dst_ports.py nccl_ports`)
sleep 10s
tcpdump -c 500000 -i enp194s0 -Q out -l dst port ${ports[0]} or ${ports[1]} or ${ports[2]} or ${ports[3]} > $1
