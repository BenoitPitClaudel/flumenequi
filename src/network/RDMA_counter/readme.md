# NIC RDMA Counter

As the tcpdump tool does not reveal the number of RDMA packets sent or recieved, this tool provides a relatively fine grained (1.6 ms / 620 Hz) sequence of RDMA counter measurements, which can then be converted into RDMA bandwidth estimates.

## Usage

1. Adjust length of file (required memory buffer size), filename scheme, and counter to read on via the following variables: `<LOOP_SIZE>`, line 12; `<filename>`, line 61; and `<fp>`, line 89 respectively.
2. Make using:
>make all 
3. Run as follows, with an integer number of repeats of `<LOOP_SIZE>` samples to give finer grained control of the length of probe to run:
>./NIC_RDMA_counter <repeat_number>
4. The output is provided in sequential files with the time elapsed per measurement and number of 32-bit words (number of data octets divided by 4) counted since the NIC counter was reset, and as such can be processed simply with a numerical difference function.

### Notes

If tighter data sample spacing is sought, multithreading, as per in the tcp client/server codebase, should enable the counter to be read faster. 