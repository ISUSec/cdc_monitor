#! /usr/bin/env python
 
from urllib2 import urlopen
import socket
from sys import argv
import struct
from ftplib import FTP
import random
import time
from threading import Thread
import datetime
import psycopg2

def tcp_test(server_info):
    cpos = server_info.find(':')
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        return True
    except:
        return False
 
def http_test(server_info):
    try:
        socket.setdefaulttimeout(1)
        data = urlopen(server_info, timeout=1).read()
        return True
    except:
        #print(e)
        return False
 
def buildDNSQuery(host):
    packet=struct.pack("!HHHHHH", 0x0001, 0x0100, 1, 0, 0, 0)
    
    for name in host:
        query=struct.pack("!b"+str(len(name))+"s", len(name), name)
        packet=packet+query
    
    packet=packet+struct.pack("!bHH",0,1,1)
    
    return packet
 
# just ask for www.google.com
TEST_QUERY=buildDNSQuery(["www","google","com"])
TIMEOUT=2
 
# scan a server for DNS
def dns_test(server_info):
    cpos = server_info.find(':')
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.settimeout(TIMEOUT)
    
    # send DNS question to server
    sendcount=s.sendto(TEST_QUERY, 0, (server_info[:cpos], int(server_info[cpos+1:])))
    if sendcount <= 0:
        return False
        
    # wait for response
    try:
        recvdata=s.recvfrom(1024)
    except socket.error, e:
        return False
            
    return True

def ftp_test(server_info):
    cpos = server_info.find(':')

    ftp = FTP()
    try:
        ftp.connect(server_info[:cpos],int(server_info[cpos+1:]),2)
    except socket.error, e:
        return False

    return True

def long_term_monitoring(test_type, server_info, team_num, service_name):
    if test_type.lower() == 'tcp':
        check = tcp_test
    elif test_type.lower() == 'http':
        check = http_test
    elif test_type.lower() == 'dns':
        check = dns_test
    elif test_type.lower() == 'ftp':
        check = ftp_test
    else:
        print("%s is not a service type." % (test_type))
        return False

    import psycopg2
    conn = psycopg2.connect("dbname='monitor'")
    cur = conn.cursor()

    i = 0
    while(i < 3):
        time.sleep(random.randint(15,45))
        if (check(server_info)):
            print('Team %d - %s - Connected to %s %s.' % (team_num, service_name, test_type, server_info))
            cur.execute("INSERT INTO events (team_num, check_name, passed, time) VALUES (%s, %s, %s, %s)", (team_num, service_name, True, datetime.datetime.now()))
            conn.commit()
        else: 
            print('Team %d - %s - Unable to connect to the service %s %s.' % (team_num, service_name, test_type, server_info))
            cur.execute("INSERT INTO events (team_num, check_name, passed, time) VALUES (%s, %s, %s, %s)", (team_num, service_name, False, datetime.datetime.now()))
            conn.commit()
        i += 1

    cur.close()
    conn.close()  


def team_check(team_num):
    Thread(target = long_term_monitoring, args = ("http", "http://www.google.com:8080", team_num, "UBUNTU WEB")).start()
    Thread(target = long_term_monitoring, args = ("http", "http://www.google.com:80", team_num, "IIS WEB")).start()
    Thread(target = long_term_monitoring, args = ("dns", "localhost:53", team_num, "DNS")).start()
    Thread(target = long_term_monitoring, args = ("ftp", "localhost:21", team_num, "FTP")).start()


def server_test(test_type, server_info):
    if test_type.lower() == 'tcp':
        return tcp_test(server_info)
    elif test_type.lower() == 'http':
        return http_test(server_info)
    elif test_type.lower() == 'dns':
        return dns_test(server_info)
    elif test_type.lower() == 'ftp':
        return ftp_test(server_info)

if __name__ == '__main__':
    '''
    if len(argv) != 3:
        print('Wrong number of arguments.')
    elif not server_test(argv[1], argv[2]):
    	print('Unable to connect to the service %s %s.' % (argv[1].upper(), argv[2]))
    '''
    conn = psycopg2.connect("dbname='monitor'")
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('events',))
    if (not cur.fetchone()[0]):
        print("Table missing!")
        cur.execute("CREATE TABLE events (id serial PRIMARY KEY, team_num integer, check_name char(20), passed boolean, time timestamp);")

    conn.commit()
    cur.close()
    conn.close()  
    team_check(1)
    #team_check(2)


