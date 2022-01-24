import numpy as np
import sys
#import re
import datetime
from collections import defaultdict
#tcpdump_output_re = re.compile(r'(?P<ts>[0-9]+:[0-9]+:[0-9]+\.[0-9]+)\sIP\s(?P<src>[0-9A-Za-z\.]+)\.(?P<src_port>[0-9]+)\s>\s(?P<dst>[0-9A-Za-z\.]+)\.(?P<dst_port>[0-9]+):.*length\s(?P<payload_length>[0-9]+)')
packet_padding = 58 
Gbps=1E-9
def parse_file(fn, parse_ports):
    bws = []
    if parse_ports:
        src_port = defaultdict(int)
        dst_port = defaultdict(int)
    ln = 0
    next_second = 1
    with open(fn) as f:
        for line in f:
            ln += 1
            try:
                ls = line.strip().split(" IP ")
                items = ls[0].split(":")
                items = [2022, 1, 1] + items[:-1] + items[-1].split(".")
                ts = datetime.datetime(*map(int, items))
                #ts = datetime.datetime.strptime(ls[0], "%H:%M:%S.%f")
                pkt = ls[1].split(" > ")
                if parse_ports:
                    dp = int(pkt[1].split(":")[0].split(".")[-1])
                    sp = int(pkt[0].split(".")[-1])
                    dst_port[dp] += 1
                    src_port[sp] += 1
                pkt_length = (packet_padding + int(pkt[1].split("length ")[-1]))*8
            except Exception as e:
                continue
            if ln == 1:
                init_ts = ts
                bws.append(pkt_length)
                continue
            else:
                elapsed = (ts - init_ts).total_seconds()
                if elapsed < 0:
                    ts = ts + datetime.timedelta(days=1)
                    elapsed = (ts - init_ts).total_seconds()
                if elapsed > next_second:
                    bws.append(pkt_length)
                    next_second = int(elapsed) + 1
                else:
                    bws[-1] += pkt_length
                final_ts = ts
    if len(bws) == 0:
        return [0], 0, None, None
    bws = [b*Gbps for b in bws]
    bws[-1] = bws[-1] / (elapsed - int(elapsed))
    avg = np.mean(bws)
    bws = [b for b in bws if (b-avg) < 0.25*avg]
    return bws, elapsed, src_port if parse_ports else None, dst_port if parse_ports else None
if __name__ == "__main__":
    parse_ports = bool(int(sys.argv[2]))
    job_rate, run_time, src_ports, dst_ports = parse_file(sys.argv[1], parse_ports)
    if parse_ports:
        print(src_ports, dst_ports)
    print("XP:{}, job rate: {}, time: {}".format(sys.argv[1], np.mean(job_rate), run_time))
