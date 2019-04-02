from socket import socket, AF_INET, SOCK_STREAM
from sys import stdout, exit
from threading import Thread
import random                                                      #IMPORT LIBRARIES
import os
import logging

buffer_size = 8192                              #Buffer Size
connected = False
logging.basicConfig(level=logging.INFO, filename='chatclient.log', format='[%(levelname)s] %(asctime)s %(threadName)s %(message)s',) 

#FUNCTION TO SEND TO SERVER

def send_to_server(sock, server_IP):
    try:
        while 1:                                #Runs on it's own thread
            msg = raw_input()
            sock.sendall(msg)
    except: 
        connected = False                       #Listens for exiting with ctrl + C
        exit(1)
    
#FUNCTION TO RECEIVE FROM SERVER

def recv_from_server(sock, server_IP):
    
    try:
        a = random.randint(1,500)               #Choose a random number between 1-500
        #print a
        logging.info("File name choosen: File{}".format(a))
        b = "File"+str(a)                       #Open file using this name
        rw = open(b, "wb")                      #Write Binary data into the file

        while 1:
            msg = sock.recv(buffer_size)
            if len(msg) < 500:                  #For chat data
                print msg
                stdout.flush()

            else:
                #print "***************"        #For large data
                #print msg 
                #print "###############"
                rw.write(msg)
        rw.close()                              #CLose file

    except: 
        connected = False                       #Listens for exiting with ctrl + C
        exit(1)


#MAIN PROGRAM WITH MULTI-THREADING

def main(argv):
    #print("CR7",argv)
    server_IP_addr ='192.168.43.110'
    server_port =8000                  #Server Port
    #print(server_IP_addr)
    #print(server_port)
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((server_IP_addr,server_port))
    connected = True
    
    send_thread = Thread(target=send_to_server, args=(sock, server_IP_addr))            #Start send thread to server
    send_thread.start()
    recv_thread = Thread(target=recv_from_server, args=(sock, server_IP_addr))          #Start receive thread from server
    recv_thread.start()
    
    try:
        while True:
            if (not connected):
                exit(1)                                         #Exit on Keyboard Interrupt
    except (KeyboardInterrupt, SystemExit):
        stdout.flush()
        print '\nConnection to server closed.'                  #Close server
        logging.info("Connection to server closed")
    
main(argv)
