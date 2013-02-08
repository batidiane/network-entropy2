import pcap
import sys
import string
import time
import socket
import struct
import dpkt
#see http://pylibpcap.sourceforge.net/

protocols={socket.IPPROTO_TCP:'tcp',
           socket.IPPROTO_UDP:'udp',
           socket.IPPROTO_ICMP:'icmp'}

def decode_ip_packet(s):
    d={}
    d['version']=(ord(s[0]) & 0xf0) >> 4
    d['header_len']=ord(s[0]) & 0x0f
    d['tos']=ord(s[1])
    d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
    d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
    d['flags']=(ord(s[6]) & 0xe0) >> 5
    d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
    d['ttl']=ord(s[8])
    d['protocol']=ord(s[9])
    d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
    d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
    d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
    if d['header_len']>5:
        d['options']=s[20:4*(d['header_len']-5)]
    else:
        d['options']=None
    d['data']=s[4*d['header_len']:]
    return d

def decodeipv4(ip):
    pktinfos = dict()
    pktinfos['src_addr'] = pcap.ntoa(struct.unpack('i',ip.src)[0])
    pktinfos['dst_addr'] = pcap.ntoa(struct.unpack('i',ip.dst)[0])
    pktinfos['proto'] = ip.p
    
    if dpkt.ip.IP_PROTO_TCP == ip.p: #Check for TCP packets
        tcp = ip.data
        pktinfos['proto_name'] = 'TCP'
        pktinfos['src_port'] = tcp.sport
        pktinfos['dst_port'] = tcp.dport
        payload = tcp.data
    elif dpkt.ip.IP_PROTO_UDP == ip.p: #Check for UDP packets
        udp = ip.data
        pktinfos['proto_name'] = 'UDP'
        pktinfos['src_port'] = udp.sport
        pktinfos['dst_port'] = udp.dport
        payload = udp.data
    elif dpkt.ip.IP_PROTO_ICMP == ip.p: #Check for ICMP packets
        icmp = ip.data
        pktinfos['proto_name'] = 'ICMP'
        pktinfos['src_port'] = 0
        pktinfos['dst_port'] = 0
        payload = str(icmp.data)
    else:
        return None, None
           
    return pktinfos, payload
    

def extractpayload(eth):
    if dpkt.ethernet.ETH_TYPE_IP == eth.type:      # ipv4 packet
        return decodeipv4(eth.data)
    elif dpkt.ethernet.ETH_TYPE_IP6 == eth.type:    # ipv6 packet
        return None, None
    elif dpkt.ethernet.ETH_TYPE_ARP == eth.type:    # arp packet
        return None, None
    elif dpkt.ethernet.ETH_TYPE_REVARP == eth.type:    # rarp packet
        return None, None
    else:
        return None, None