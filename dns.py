# dnsfind.py <startip> <endip>
 
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
def ScanDNS(addr, timeout):
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
 
# extract an ip address into a tuple of integers
def ExtractIP(ip):
	partip=ip.split(".")
	if len(partip) != 4:
		print "Invalid ip address: "+ip
	try:
		iptuple=(int(partip[0]),int(partip[1]),int(partip[2]),int(partip[3]))
	except ValueError:
		print "Invalid ip address: "+ip
		
	return iptuple
 
if len(sys.argv) < 2:
	print "Not enough parameters supplied!"
 
# convert ip address to integer tuple
START_IP=ExtractIP(sys.argv[1])
END_IP=ExtractIP(sys.argv[2])
 
# store found DNS servers
foundDNS=[]
 
# scan all the ip addresses in the range
for i0 in range(START_IP[0], END_IP[0]+1):
	for i1 in range(START_IP[1], END_IP[1]+1):
		for i2 in range(START_IP[2], END_IP[2]+1):
			for i3 in range(START_IP[3], END_IP[3]+1):
				# build ip addres
				ipaddr=str(i0)+"."+str(i1)+"."+str(i2)+"."+str(i3)
				
				print "Scanning "+ipaddr+"...",
				
				# scan address
				ret=ScanDNS(ipaddr, 10)
				
				if ret==True:
					foundDNS.append(ipaddr)
					print "Found!"
				else:
					print 
 
# print out all found servers
print "--------------------------------------------------------"
print "DNS Servers:"
 
for dns in foundDNS:
	print dns
