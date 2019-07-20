#import socket
#from time import sleep
import ctypes
import numpy as np
#  
#UDP_PORT = 49122
#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.connect(('192.168.1.101', UDP_PORT))
#  
#while True:
#    sock.send(b'Hello, World!')
#    sleep(1)

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Make the socket multicast-aware, and set TTL.
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
     # Send the data
   
    
#while True:
#s.sendto('hello'.encode(), ('169.254.104.146', 49122))
s.sendto(bytes([255, np.uint8(255), 0,0]), ('169.254.104.146', 49122))
#sleep(1)