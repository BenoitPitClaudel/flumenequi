import numpy as np
import paramiko
import re
import datetime
from collections import defaultdict
from time import time
import sys
tcpdump_output_re = re.compile(r'(?P<ts>[0-9]+:[0-9]+:[0-9]+\.[0-9]+)\sIP\s(?P<src>[0-9A-Za-z\.]+)\.(?P<src_port>[0-9]+)\s>\s(?P<dst>[0-9A-Za-z\.]+)\.(?P<dst_port>[0-9]+):.*, seq (?P<seq>[0-9:]+), ack (?P<ack>[0-9]+), win (?P<win>[0-9]+), length\s(?P<payload_length>[0-9]+)')
IP_TABLE = {"juno": "172.32.10.1",
            "kasra": "172.32.11.1",
            "liangyu": "172.32.12.1"}
INVERTED_IP_TABLE = {v: k for k, v in IP_TABLE.items()}

class Trace:
    def __init__(self, xp):
        self.flows = defaultdict(list)
        self.packet_delays = defaultdict(list)
        self.xp_identifier = xp
        self.stats = {}

    def add_packet(self, packet):
        id_tuple = (packet.srcIP, packet.srcPort, packet.dstIP, packet.dstPort, packet.loggedAt)
        self.flows[id_tuple].append(packet)

    def in_order_sanity_check(self):
        for flow in self.flows:
            for i in range(len(self.flows[flow]) - 1):
                assert self.flows[flow][i + 1].time >= self.flows[flow][i].time, "{}".format((self.flows[flow][i+1], self.flows[flow][i]))
        print("Flow was logged in order")

    def match_packets(self):
        print(set((k[:-1]) for k in self.flows.keys()))
        for id_tuple in set((k[:-1]) for k in self.flows.keys()):
            delays = []
            retransmits = 0
            total_packet_pairs = 0
            unmatch_received_packets = 0
            first_match = False
            packets_before_first_match = 0
            src_flow = self.flows[(*id_tuple, id_tuple[0])]
            dst_flow = self.flows[(*id_tuple, id_tuple[2])]
            print(id_tuple, len(src_flow), len(dst_flow))
            i_s = 0
            for i_d, p in enumerate(dst_flow):
                # print(i_s, i_d)
                for i_cur in range(i_s, len(src_flow)):
                    if src_flow[i_cur].time > p.time + datetime.timedelta(milliseconds=10):
                        if first_match:
                            unmatch_received_packets += 1
                        else:
                            packets_before_first_match += 1
                        break
                    if src_flow[i_cur] == p:
                        retransmits += i_cur - i_s
                        i_s = i_cur + 1
                        total_packet_pairs += 1
                        delays.append((p.time - src_flow[i_cur].time).total_seconds())
                        first_match = True
                        break

            self.packet_delays[id_tuple] = delays
            self.stats[id_tuple] = {"retransmits": retransmits,
                                    "total_packet_pairs": total_packet_pairs,
                                    "unmatch_received_packets": unmatch_received_packets,
                                    "before_first_match": packets_before_first_match}
            if retransmits + total_packet_pairs == len(src_flow) and unmatch_received_packets + total_packet_pairs + packets_before_first_match == len(dst_flow):
                print("Flow OK")
            else:
                print("Flow does not add up")
                print(self.stats)
            
    def show_stats(self):
        print("XP:{}, means: {}, global mean: {}, number of logged packets: {}\n".format(self.xp_identifier, list(map(np.mean, self.packet_delays.values())), np.mean([v for d in self.packet_delays for v in self.packet_delays[d]]), sum([len(v) for v in self.packet_delays.values()])))
class Packet:
    def __init__(self, log_origin, timestamp, srcIP, srcPort, dstIP, dstPort, seq, ack, win, length):
        self.loggedAt = IP_TABLE[log_origin]
        self.time = datetime.datetime.strptime(timestamp, "%H:%M:%S.%f")
        self.srcIP = IP_TABLE[srcIP] if srcIP in IP_TABLE else srcIP
        self.dstIP = IP_TABLE[dstIP] if dstIP in IP_TABLE else dstIP
        self.srcPort = int(srcPort)
        self.dstPort = int(dstPort)
        self.seq_start, self.seq_end = map(int, seq.split(":")) if len(seq.split(":")) == 2 else (int(seq), int(seq))
        self.ack = int(ack)
        self.win = int(win)
        self.length = int(length)

    def __eq__(self, other):
        return self.srcIP == other.srcIP and self.dstIP == other.dstIP and self.srcPort == other.srcPort\
               and self.dstPort == other.dstPort and self.seq_start == other.seq_start and self.seq_end == other.seq_end

    def __str__(self):
        return "{}: {}, {}.{} -> {}.{}, {}:{}".format(INVERTED_IP_TABLE[self.loggedAt], self.time, INVERTED_IP_TABLE[self.srcIP], self.srcPort, INVERTED_IP_TABLE[self.dstIP], self.dstPort, self.seq_start, self.seq_end)

    def __repr__(self):
        return self.__str__()
def experiment(identifier, servers):
    trace = Trace(identifier)
    for server in servers:
        if server == "kasra":
            remote_file = open(identifier)
        else:
            start = time()
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_agent = paramiko.agent.Agent()
            for k in ssh_agent.get_keys():
                if k.name == "ssh-rsa":
                    key = k
            ssh_client.connect(hostname='{}.csail.mit.edu'.format(server),username='benoit', pkey=key)
            sftp_client = ssh_client.open_sftp()
            # print('pollux/flumenequi/traffic_logs/{}'.format(identifier))
            remote_file = sftp_client.open('pollux/flumenequi/traffic_logs/{}'.format(identifier))
            # print("time to open ssh and load file:", time() - start)
        try:
            i = 0
            start = time()
            for line in remote_file:
                i += 1
                m = tcpdump_output_re.match(line)
                if not m:
                    print("Regex failed on line: ", line)
                    continue
                else:
                    trace.add_packet(Packet(server, *m.groups()))
                # if i % 1000 == 0:
                    # print("time for 1000 iteration: ", time() - start)
                    # start = time()
                if i > 20000:
                    break
        finally:
            remote_file.close()
            # print("finished {}/{}".format(server, identifier))

    return trace

trace = experiment(sys.argv[1], ["juno", "kasra", "liangyu"])
# trace.in_order_sanity_check()
trace.match_packets()
trace.show_stats()
