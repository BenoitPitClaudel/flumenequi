#!/usr/bin/env bash
if [[ "$#" -ne 2 ]]; then
    echo "Usage: ./connect.sh server_id ip_prefix"
    exit 2
fi
ip link set dev enp194s0 up
ip address add "$2"."$1".1/24 dev enp194s0
ip route add "$2".0.0/16 via "$2"."$1".2
