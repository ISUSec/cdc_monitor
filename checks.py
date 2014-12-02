#! /usr/bin/env python
 
from urllib2 import urlopen
from socket import socket
from sys import argv
import sys
import socket
import struct

# basic DNS header for 1 query
def buildDNSQuery(host):
	packet=struct.pack("!HHHHHH", 0x0001, 0x0100, 1, 0, 0, 0)
	
	for name in host:
		query=struct.pack("!b"+str(len(name))+"s", len(name), name)
		packet=packet+query
	
	packet=packet+struct.pack("!bHH",0,1,1)
	
	return packet
 
# just ask for www.google.com
TEST_QUERY=buildDNSQuery(["www","google","com"])
DNS_PORT=53
TIMEOUT=2
 
# scan a server for DNS
def dns_test(addr):
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
	s.settimeout(TIMEOUT)
	
	# send DNS question to server
	sendcount=s.sendto(TEST_QUERY, 0, (addr,DNS_PORT))
	if sendcount <= 0:
		return False
		
	# wait for response
	try:
		recvdata=s.recvfrom(1024)
		print(recvdata)
	except socket.error, e:
		print(e)
		return False
			
	return True
 
 
def tcp_test(server_info):
    cpos = server_info.find(':')
    try:
        sock = socket()
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        return True
    except:
        return False
 
def http_test(server_info):
    try:
        data = urlopen(server_info).read()
        return True
    except:
        return False

 
 
def server_test(test_type, server_info):
    if test_type.lower() == 'tcp':
        return tcp_test(server_info)
    elif test_type.lower() == 'http':
        return http_test(server_info)
