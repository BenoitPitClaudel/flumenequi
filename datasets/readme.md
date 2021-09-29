# Processed Data Used in Figures

This folder contains the processed data used to generate the figures present in each excel spreadsheet present. Where available, the output files of the processing scripts are included as '*.csv' files to assist in reuse. Further processing taken to produce plots is described within the spreadsheets themselves. All results were generated utilizing a 25 Gbps network.

## iperf Data

The folder 'iperf' contains data and figures for distributed learning on RDMA competing against iperf traffic runs from 0 to 25 Gbps. Models: ResNet-50, DenseNet-161, VGG-16, BERT-large.

## Consistent Web-search Data

The folder 'consistent_ws' contains data and figures for distributed learning on RDMA competing against consistent web-search data runs from 0 to 25 Gbps. Models: ResNet-50, DenseNet-161, VGG-16, BERT-large.

## Burst Web-search Data

The folder 'burst_ws' contains data and figures for distributed learning on TCP competing against the 300% peak, 1 ms width, bursty web-search data runs from 0 to 25 Gbps. Models: ResNet-50, DenseNet-161, VGG-16, BERT-large.

## Cumulative Density Function

The folder 'cdfs' contains data and figures for CDFs at 8 and 20 Gbps (roughly 30% and 80% load). Runs are conducted for consistent web-search cross traffic on TCP and RDMA, and burst web-search cross traffic on TCP. Models: ResNet-50, VGG-16, BERT-large.

## Comparison

The folder 'comparisons' contains data and figures for distributed learning on TCP competing against the consistent web-search data runs from 0 to 25 Gbps for ResNet-50 and BERT-large models. Fits and associated calculations also included in this excel spreadsheet.

## Histogram

The folder 'histogram' contains data and figures for histograms of the instantaneous packet inject rate for consistent and burst traffic at an exemplar rate of 24 Gbps. 

## Instantaneous Packet Injection Rates

The folder 'instantaneous' contains data for the instantaneous packet injection rate over a short, synchronized portion of a run. These are graphed into figures displaying the relative rates across three flows at low and high cross traffic levels (8, 20 Gbps) for models ResNet-50 and BERT-large. Longer processed run-data is not included due to size constraints. 

Fresh runs can be produced using the method described [here](/src/processing/readme.md) using the [sync_instant_tcpdump_processing.py](/src/processing/sync_instant_tcpdump_processing.py) script

## Samples of Burst and Consistent Web-search Traffic, and a Generated Load File

The folder 'sample_loads' contains plots of the instantaneous packet injection rate for consistent and burst web-search traffic against time, to give a sense of the behavior and characteristics of each load type. The generated load file gives an example of the profile of requested flows produced by the load generation scripts that accompany the flumenequi load tool.