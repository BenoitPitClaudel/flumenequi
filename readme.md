# Flumen Equi - A characterization of Network Requirements for Distributed Machine Learning in the Cloud

This repository, named Horses River in Latin as an allusion to the significant number of packets, flows, and processes that make up the overall communication stream of distributed learning training, contains the results of my characterization of the response of Distributed Machine Learning (DL) training to the presence of competing 'cross' traffic.

## Structure

This repository is broken down into three key sections:
1. The [processed datasets](datasets) that contain the figures from my thesis and the data and final processing details that go into them, along with *.csv files of the data for convenient reuse. Additional information on [datasets](datasets/readme.md).
2. The [code](src) used to perform [DL training](src/distributed_learning/readme.md) and create [cross traffic](src/network/readme.md) as well as the [processing code](src/processing/readme.md) required to interpret the raw outputs.
3. [Run scripts](run_scripts/readme.md) for the general case and notes on how to run each type of experiment I have performed.

## Technical Notes

### Network Topology

I utilize two toy network topologies to collect the data in the [datasets](datasets) folder, A, with egress as the bottleneck and B, with ingress as the bottleneck, as shown in the Topology figure below. The majority of data is captured using configuration B, to ensure the bottleneck exists in the switch (network) side, rather than on a server's NIC. This is an important consideration for replicating these results.

![Topology](https://github.com/hipersys-team/james-flumenequi/blob/a7a17968634e2b65705f083c9b01215fa8df53af/datasets/topology.pdf)

### Infrastructure and Versions

I captured these results on a cluster of four ASUS ECS4000A-E10 servers. Each is fitted with an AMD EPYC 7502P 32-core processor, an Nvidia A100 accelerator with 40 GB of HBM2e memory. Networking is provided by Mellanox ConnectX-5 100 Gbps NICs on each server directly connected to a Juniper MX480 SDN Switch. The switch is configured to 25 Gbps mode for this cluster, which means each NIC also reports the available link speed as 25 Gbps. I made this choice to explore the impacts of high network congestion levels between reasonably sized DL loads and cross traffic at a significant link capacity, without needing to be concerned about additional bottlenecks or confounding factors present at the full 100 Gbps system capability. I utilized Ubuntu 18.04, CUDA v11.1, cuDNN v8.0.5 and NCCL v2.7.8, Horovod v0.21.3, Pytorch v1.7.1 and Tensorflow v2.4.1.