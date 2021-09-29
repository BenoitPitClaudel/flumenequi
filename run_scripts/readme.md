# Run Scripts

## Data gathering

In order to run an arbitrary experiment from this dataset, one must start 4 processes:

1. The DL task (which includes iteration logging)
2. The N web-search server processes
3. The top client server process
4. tcpdump (which performs bandwidth logging)

The first two tasks are typically performed on the same machine, while the second two are also performed on the same machine. An example [script](auto_run.sh) to run all 4 tasks using SSH can be called as follows:

>. ./auto_run.sh

This runs the script in the existing terminal, and allows the 'fg' and 'ctrl-c' commands to be used to terminate the tcp client and monitor and the machine learning task at the end of the experiment. The user only needs to specify the model, load, and iteration/tcp log locations in both the base auto_run.sh script and the client_run.sh script it calls to run the complete suite of experiments.

## Processing

Processing can be done on a server or a local machine. For efficiency and the size of tcpdump log files, I recommend that tcpdump processing is done on the server end. A batch processing [file](batch_processing.sh) allows straight-forward simultaneous processing. Note that to obtain some data, as described in the processing [readme](/src/processing/readme.md), tweaks are required, for example iteration log truncation, or filter length adjustments for tcpdump log processing.

## Recreation of Datasets

The consistent and burst web-search datasets can be recreated directly using the provided [auto_run](auto_run.sh) script, substituting the desired load values, and specifying at load generation the length of experiment desired. The iperf dataset can likewise be recreated by substituting the load section for an iperf stream. 

The CDFs and histograms are produced by running the raw data obtained from these runs through different processing files. Detailed instructions are available in the [processing readme](/src/processing/readme.md).

The instantaneous dataset, and sample_loads dataset, are both taken directly from lightly processed tcpdump observations from specific network points. Thus, to recreate this data, again utilize the appropriate [processing](/src/processing/sync_instant_tcpdump_processing.py) file, and perform a tcpdump from 3 (or more, with modifications to the processing file) locations in your network configuration that are of interest.

## Individual Operation

Common run commands required to operate individual portions of code/experiments are provided here for convenience:

- Simultaneous File Limit: 
>ulimit -n 24096
- TCP Client: 
>./client < path/to/load.config
- TCP Server: 
>./server port_number & (default is 81808X)
- tcpdump: 
>sudo tcpdump -i enp194s0 -Q out -l > path/to/log
- Iperf: 
>Server: iperf -s
>Client: iperf -c ip -b bw -t time -i printing_time -P parallel
- Machine Learning (Imagenet): 
>mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot \
>--mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 \
>--mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H abtin:1,bly:1,dara:1 -x NCCL_IB_DISABLE=1 \
>-x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV \
>python /path/to/james-flumenequi/src/distributed_learning/pytorch_imagenet.py --synth -a <resnet50/densenet161/vgg16> \
>--epochs 1 -p 1 -b 64 > path/to/log
- Machine Learning (NLP): 
>mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot \
>--mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp --mca btl_tcp_if_include enp3s0f0 \
>--mca pml ^ucx --mca mtl ^ofi --mca coll ^hcoll --np 3 -H abtin:1,bly:1,dara:1 -x NCCL_IB_DISABLE=1 \
>-x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH -x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV \
>python /path/to/james-flumenequi/src/distributed_learning/pytorch_NLP_hvd.py  > path/to/log
- Iteration Time Processing: 
>python /path/to/james-flumenequi/src/processing/pytorch_iter_time_processing.py consistent_logs/iter_consistent_rn50_23G.txt 23 0 10 >> consistent_logs/processed/iter_consistent_rn50_proc.csv