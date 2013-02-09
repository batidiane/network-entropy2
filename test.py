#!/usr/bin/python
from IO.io import *
import IO
import libpcap
import Algorithm
import pcap
import sys
import string
import time
import socket
import struct
from libpcap.packet import *
import sys
import string
import struct
import argparse

#see http://pylibpcap.sourceforge.net/


output_class_name = ''
algorithm_list = [] #algorithms to be loaded
keys_to_calculate = []
keys_to_print = []


def execute(inputdata,  algorithm):
    inputdata.apply_function(keys_to_calculate, algorithm) 
    #inputdata.add('algorithm', algorithm.getName())
    #return inputdata

def analysepacket(pktlen, data, timestamp):
    global out_list
    global algorithm_list
    global output_class_name
    if not data:
        return
    
    #inputpacket = InputIPPacket(decode_ip_packet(data))
    pktinfos, payload = extractpayload(dpkt.ethernet.Ethernet(data))
    if pktinfos and payload:
        inputpacket = IPPacket(pktinfos, payload, timestamp)
        for algo in algorithm_list:
            execute(inputpacket, algo)
        inputpacket.printData(keys_to_print)
            
def load_algorithm(algorithm_name):
    global algorithm_list
    #keys_to_print.append(algorithm_name)
    for mod_name in Algorithm.__all__:
        mod = __import__('Algorithm.'+mod_name, fromlist=Algorithm.__all__)
        mod_instance = getattr(mod, mod_name)()
        try:
            if algorithm_name == mod_instance.getName():
                algorithm_list.append(mod_instance)
        except:
            pass
def load_algorithms(algorithm_names):
    for name in algorithm_names:
        load_algorithm(name)
        
if __name__ == "__main__":
    #text = InputFile("fichiertest.txt")
    #out = execute(text, 'ConsoleOutput', "ShannonEntropy")
    #out.printOutput()
    global out_list
    global algorithm_list
    global output_class_name
    global keys_to_calculate
    global keys_to_print
    keys_to_print.append('src_addr')
    keys_to_print.append('dst_addr')
    keys_to_print.append('proto_name')
    #keys_to_print.append('algorithm')
    keys_to_print.append('payload entropy')
    keys_to_print.append('timestamp')
    
    keys_to_calculate.append('payload')
    output_class_name = 'Data'
    #load_algorithm('shannon')
    parser = argparse.ArgumentParser(description='Calculate entropy from live capture or pcap file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--interface', dest='interface', help='live capture from an interface (default:lo)')
    group.add_argument('-f', '--file', dest='pcapfile', help='filename of a capture file to read from')
    parser.add_argument('-a', '--algo', dest="algo", help='entropy algorithm. 2 choices: "sha" for shannon entropy or "kol" for kolmogorov')
    parser.add_argument('bpf', help='BPF filter like "tcp and port 22"')
    options = parser.parse_args()
    
    if options.interface:
        interface = options.interface
        live = True
    elif options.pcapfile:
        interface = options.pcapfile
        live = False
    else:
        interface = 'lo'
        live = True
    
    if options.algo:
        algorithms = options.algo
    load_algorithms(algorithms.split())
    bpf = options.bpf
    p = pcap.pcapObject()
    if True == live :
        net, mask = pcap.lookupnet(interface)
        p.open_live(interface, 65535, 0, 50)
    else:
        p.open_offline(interface)
    p.setfilter(bpf, 0, 0)

    # try-except block to catch keyboard interrupt.  Failure to shut
    # down cleanly can result in the interface not being taken out of promisc.
    # mode
    try:
        while 1:
            p.dispatch(1, analysepacket)
            
    except KeyboardInterrupt:
        print '%s' % sys.exc_type
        print 'shutting down'
        print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()
