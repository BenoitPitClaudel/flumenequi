import sys
from collections import defaultdict, Counter
def parse_most_common_ports(fn):
    dst_port = defaultdict(int)
    other = 0
    bg_out_length = 0
    job_out_length = 0
    ln = 0
    with open(fn) as f:
        for line in f:
            try:
                ls = line.strip().split(" IP ")
                pkt = ls[1].split(" > ")
                dp = int(pkt[1].split(":")[0].split(".")[-1])
                dst_port[dp] += 1
            except Exception as e:
                continue
    ports = list(zip(*Counter(dst_port).most_common(4)))[0]
    return list(ports)
if __name__ == "__main__":
    print("{} {} {} {}".format(*parse_most_common_ports(sys.argv[1])))
