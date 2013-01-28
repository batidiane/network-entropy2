from Algorithm.ShannonEntropy import ShannonEntropy
from IO.io import ConsoleOutput, InputFile, InputIPPacket
import libpcap
import Algorithm
import IO
import pcap
import sys
import string
import time
import socket
import struct
from libpcap.packet import decode_ip_packet

#see http://pylibpcap.sourceforge.net/
def execute(inputdata, outputclass, algorithmclass):
    #module = __import__('Algorithm', fromlist='ShannonEntropy')
    #module = __import__('Algorithm.%s'%algorithmclass,fromlist=['Algorithm'])
    module = __import__('Algorithm.'+algorithmclass, fromlist=Algorithm.__all__)
    algorithm = getattr(module, algorithmclass)()
    module2 = __import__('IO.io', fromlist=IO.__all__)
    outputdata = getattr(module2, outputclass)(algorithm.getName())
    data = inputdata.getData()
    for key in data:
        entropy = algorithm.calculate(data[key])
        outputdata.add(key, entropy)
    return outputdata

def capture(pktlen, data, timestamp):
    if not data:
        return
    if data[12:14]=='\x08\x00':
        inputpacket = InputIPPacket(decode_ip_packet(data))
        out = execute(inputpacket, 'ConsoleOutput', "ShannonEntropy")
        out.printOutput()
        
if __name__ == "__main__":
    #text = InputFile("fichiertest.txt")
    #out = execute(text, 'ConsoleOutput', "ShannonEntropy")
    #out.printOutput()
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