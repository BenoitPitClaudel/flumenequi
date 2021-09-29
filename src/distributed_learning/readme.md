# Distributed Learning Running

## First Time Setup:

1. Verify you have a local installation of the following:
    - 'cmake' - eg 3.21.1
    - 'mpirun' - eg 4.1.1
    - NCCL - appropriate for GPU
    - 'cuda' - appropriate for GPU
2. Verify 'nvidia-smi' shows expected consistent versions across all servers
3. Build a conda environment from [hvd_21_environment.yml](hvd_21_environment.yml)
4. Check CUDA, CUPTI, mpirun are in the path and library path
5. Run 'horovodrun -cb' to check the horovod build, ensure you see a check against: Pytorch (framework), MPI (controller) and NCCL (tensor operations).

Horovod can be debugged and reinstalled from their [github](https://github.com/horovod/horovod#install)

## To Run:

All imagenet models are bundled into one file, BERT is in a separate file, which can be adapted fairly easily to other NLP models of interest from the hugging-face repository.

A typical run command, utilizing TCP traffic for transport, run on a single server, would have the following form for imagenet:

>mpirun --allow-run-as-root --tag-output -bind-to none -map-by slot \
>--mca osc ^ucx --mca btl_basverbose 50 --mca btl self,tcp \
>--mca btl_tcp_if_include enp3s0f0 --mca pml ^ucx --mca mtl ^ofi \
>--mca coll ^hcoll --np 3 -H abtin:1,bly:1,dara:1 -x NCCL_IB_DISABLE=1 \
>-x NCCL_DEBUG=INFO -x NCCL_SOCKET_IFNAME=enp194s0 -x PATH \
>-x LD_LIBRARY_PATH -x CONDA_DEFAULT_ENV \
>python /path/to/file/pytorch_imagenet.py --synth \
>-a <model> --epochs 1 -p 1 -b 64 > /path/to/logging/files/logfile_iter_model_label.txt

For BERT, the last two lines would be swapped for the line below:

>python /path/to/file/pytorch_NLP.py > /path/to/logging/files/logfile_iter_model_label.txt

To switch to RDMA, if available (verify with, for example, ibstat), remove the following flags:
>-x NCCL_IB_DISABLE=1 

and add the following flags:
>-x NCCL_IB_GID_INDEX=3 -x NCCL_IB_HCA=mlx5_0