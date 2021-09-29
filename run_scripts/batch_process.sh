#!/bin/bash

#set path to processing file, and appropriate processing file as required, ensure results folder exists before running script
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_2G.txt 2 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_4G.txt 4 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_6G.txt 6 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_8G.txt 8 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_10G.txt 10 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_12G.txt 12 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_13G.txt 13 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_14G.txt 14 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_15G.txt 15 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_16G.txt 16 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_17G.txt 17 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_18G.txt 18 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_19G.txt 19 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_20G.txt 20 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_21G.txt 21 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_22G.txt 22 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_23G.txt 23 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
python /path/to/james-flumenequi/src/processing/tcpdump_processing.py  ~/consistent_logs/tcp_consistent_resnet_24G.txt 24 50000 30 >> ~/consistent_logs/processed/resnet50_consistent_bw.txt &
