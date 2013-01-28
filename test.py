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
from libpcap.packet import decode_ip_packet

#see http://pylibpcap.sourceforge.net/

out_list = {} #global dict contains all result (output)
output_class_name = ''
algorithm_list = [] #algorithms to be loaded


def execute(inputdata, outputclass, algorithm):
    module = __import__('IO.io', fromlist=IO.__all__)
    outputdata = getattr(module, outputclass)(algorithm.getName())
    data = inputdata.getData()
    for key in data:
        entropy = algorithm.calculate(data[key])
        outputdata.add(key, entropy)
    return outputdata

def capture(pktlen, data, timestamp):
    global out_list
    global algorithm_list
    global output_class_name
    if not data:
        return
    if data[12:14]=='\x08\x00':
        for algo in algorithm_list:
            inputpacket = InputIPPacket(decode_ip_packet(data))
            out = execute(inputpacket, output_class_name, algo)
            out.printOutput()
            if algo.getName() in out_list:
                out_list[algo.getName()].append(out)
            else:
                out_list[algo.getName()] = []
                out_list[algo.getName()].append(out)
            
def load_algorithm(algorithm_name):
    global algorithm_list
    module = __import__('Algorithm.'+algorithm_name, fromlist=Algorithm.__all__)
    algorithm = getattr(module, algorithm_name)()
    algorithm_list.append(algorithm)
        
def statistics(final_list, classname):
    module = __import__('IO.io', fromlist=IO.__all__)
    #outputstats = getattr(module, classname)('Statistics')
    for key in final_list:
        outputstats = getattr(module, classname)('Statistics average '+key)
        count = 0
        for i in final_list[key]:
            count += 1
            for attr, value in i.getData().items():
                #print attr+'='+str(value)
                outputstats.add(attr, value)
        for attr, value in outputstats.getData().items():
            outputstats.getData()[attr] = value / count
        outputstats.printOutput()
        
if __name__ == "__main__":
    #text = InputFile("fichiertest.txt")
    #out = execute(text, 'ConsoleOutput', "ShannonEntropy")
    #out.printOutput()
    global out_list
    global algorithm_list
    global output_class_name
    output_class_name = 'ConsoleOutput'
    load_algorithm('ShannonEntropy')
    if len(sys.argv) < 3:
        print 'usage: sniff.py <interface> <expr>'
        sys.exit(0)
    
    p = pcap.pcapObject()
    #dev = pcap.lookupdev()
    dev = sys.argv[1]
    net, mask = pcap.lookupnet(dev)
    # note:  to_ms does nothing on linux
    p.open_live(dev, 1600, 0, 100)
    #p.dump_open('dumpfile')
    p.setfilter(string.join(sys.argv[2:],' '), 0, 0)
    try:
        while 1:
            p.dispatch(1, capture)
            #apply(capture, p.next())
    except KeyboardInterrupt:
        print '%s' % sys.exc_type
        print 'shutting down'
        print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()
        statistics(out_list, 'ConsoleOutput')