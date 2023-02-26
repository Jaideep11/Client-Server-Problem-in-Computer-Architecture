import socket
import sys
import time
from helper import ip_checksum

HOST = ''  
PORT = 1024 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
expect_seq = 0
timeout_test = True

while 1:
    data, addr = s.recvfrom(1024)
    
    checksum = data[:2]
    seq = data[2]
    pkt = data[3:]

    if not data:
        break
    if ip_checksum(pkt) == checksum and seq == str(expect_seq):
        print('recv: Good Data Sending ACK' + str(seq))
        print('recv pkt: ' + str(pkt))
        if str(pkt) == 'Message 4':
            time.sleep(5)
        s.sendto(str(seq), addr)
        expect_seq = 1 - expect_seq
    else:
        if seq == str(expect_seq):
            print('recv: Bad Checksum Not Sending')
        else:
            print('recv: Bad Seq Sending ACK' + str(1 - expect_seq))
            s.sendto(str(1 - expect_seq), addr)
s.close()

