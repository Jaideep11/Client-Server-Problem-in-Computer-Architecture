import socket
import sys
from socket import timeout
import helper
from helper import ip_checksum

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 8080

s.settimeout(3)
seq = 0

checksum_test = True


for i in range(7):
    message = 'Message ' + str(i)
    ack_received = False
    while not ack_received:
        try:
            if i == 3 and checksum_test:
                print('send: TESTING BAD CHECKSUM')
                s.sendto(ip_checksum("wrong") + str(seq) + message, (host, port))
                checksum_test = False
            else:
                print('send: SENDING PKT')
                s.sendto(ip_checksum(message.encode('utf-8')) + str(seq) + message, (host, port))
        except socket.error as message:
            print('Error Code : ' + str(message[0]) + ' Message ' + message[1])
            sys.exit()

        try:
            print('send: GETTING ACK')
            reply, addr = s.recvfrom(1024)
            ack = reply[0]
        except timeout:
            print('send: TIMEOUT')
        else:
            print('Checking for ACK ' + str(seq))
            if ack == str(seq):
                ack_received = True
    print('ACK FOUND, CHANGING SEQ')
    seq = 1 - seq
