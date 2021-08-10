#ACHYUTA KRISHNA V - 2018A7PS0165H
#ANIRUDH G - 2018A7PS0217H
#AJITH P J - 2018A7PS0040H
#J ALVIN RONNIE - 2018A7PS0029H
#MANEESH REDDY - 2018A7PS0462H

import sys
import signal
from socket import *
import threading
from struct import *
import socket, pickle
import os
from time import time
from time import sleep
import bitstring
import struct
from bitstring import BitArray
import random

def getack():
    global flagz
    if flagz==1:
        return
    recv_pkt, clientaddr = s.recvfrom(4096)
    print("ack recv",recv_pkt)
    dv = getHeader(recv_pkt)
    temparr = BitArray(uint=dv[0], length=8)
    ackbit = bytes(temparr)[1]
    if (ackbit == 1):
        flagz = 1
        return
def getfin():
    global flagf
    if flagf==1:
        return
    recv_pkt, clientaddr = s.recvfrom(4096)
    print("fin recv",recv_pkt)
    dv = getHeader(recv_pkt)
    temparr = BitArray(uint=dv[0], length=8)
    finbit = bytes(temparr)[2]
    if (finbit == 1):
        flagf = 1
        return


def getackdata():
    global flag
    global file_name
    global client_seq
    if flag == 1:
        return
    recv_pkt, clientaddr = s.recvfrom(4096)
    print("ackdata recv",recv_pkt)
    dv = getHeader(recv_pkt)
    if(dv == None):
        return
    temparr = BitArray(uint=dv[0], length=8)
    databit = bytes(temparr)[3]
    ackbit = bytes(temparr)[1]
    if ((ackbit == 1) and (databit == 1)):
        flag = 1
        file_name_encoded = getData(recv_pkt)
        #print(file_name_encoded)
        file_name = file_name_encoded.decode('utf8')
        print(file_name)
        #print(file_name.decode('utf8'))
        client_seq = dv[3]
        return


def encodeHeader(a,b,c,d):
    header = chr(a) + chr(b) + chr(c) + chr(d)
    return header.encode('utf8')
def encodeSynHeader(a,b,c,d,e,f,g,h,i,j,k,l):
    rt = BitArray(uint = g, length=16)
    tempg = ""
    for q in bytes(rt):
     tempg = tempg + str(q)

    ct = BitArray(uint = h, length=16)
    temph = ""
    for q in bytes(ct):
     temph = temph + str(q)

    nt = BitArray(uint = i, length=16)
    tempi = ""
    for q in bytes(nt):
     tempi = tempi + str(q)

    cid = BitArray(uint = l, length=32)
    templ = ""
    for q in bytes(cid):
     templ = templ + str(q)

    header = chr(a) + chr(b) + chr(c) + chr(d) + chr(e) + chr(f)
    header = header + chr(int(tempg[0:len(tempg)//2],2)) + chr(int(tempg[len(tempg)//2:len(tempg)],2))
    header = header + chr(int(temph[0:len(temph)//2],2)) + chr(int(temph[len(temph)//2:len(temph)],2))
    header = header + chr(int(tempi[0:len(tempi)//2],2)) + chr(int(tempi[len(tempi)//2:len(tempi)],2))
    header = header + chr(j) + chr(k)
    header = header + chr(int(templ[0:len(templ)//4],2)) + chr(int(templ[len(templ)//4:len(templ)//2],2)) + chr(int(templ[len(templ)//2:(3*(len(templ)//4))],2)) + chr(int(templ[(3*(len(templ)//4)):len(templ)],2))
    return header.encode('utf8')

def getHeader(pkt):
    recvpkt = pkt[0:4].decode('utf8')
    header = recvpkt[0:4]
    ans = []
    i = 0
    if(len(header) != 4):
    	return
    while(i<4):
     ans.append(ord(header[i]))
     i+=1
    return ans

def getData(pkt):
    #recvpkt = pkt.decode('utf8')
    #data = recvpkt[4:].encode('utf8')
    data = pkt[4:]
    return data

def getSynHeader(pkt):
    recvpkt = pkt.decode('utf8')
    ans = []
    i = 0
    while i < 6:
     ans.append(ord(recvpkt[i]))
     i = i + 1

    ans.append((ord(recvpkt[6])*256) + (ord(recvpkt[7])))
    ans.append((ord(recvpkt[8])*256) + (ord(recvpkt[9])))
    ans.append((ord(recvpkt[10])*256) + (ord(recvpkt[11])))
    ans.append(ord(recvpkt[12]))
    ans.append(ord(recvpkt[13]))
    ans.append((ord(recvpkt[14])*16777216) + (ord(recvpkt[15])*65536) + (ord(recvpkt[16])*256) + ord(recvpkt[17]))
    return ans

def getSynData(pkt):
    recvpkt = pkt.decode('utf8')
    data = recvpkt[18:].encode('utf8')
    return data

server_seq=0
server_acknum=0
client_seq=0
client_acknum=0
N = int(sys.argv[2])
MSS = int(sys.argv[3])
TIMEOUT = 5
seq_num = 0
first_in_window = -1
last_in_window = -1
last_acked = -1
num_acked = -1
send_complete = 0 
ack_complete = 0 
total_acks = 0
send_buffer = [] 
timeout_timers = [] 
acked = [] 
retrans = []
def getACKs():
    global ack_complete
    global send_complete
    global last_acked
    global last_in_window
    global first_in_window
    global send_buffer
    global N
    global s
    global acked
    global num_acked

    
    while ack_complete == 0:
        recv_pkt, serverAddress = s.recvfrom(4096)
        dv = getHeader(recv_pkt)
        temparr = BitArray(uint=dv[0], length=8)
        databit = bytes(temparr)[3]
        if databit == 1:
            return
        
        ack_num = dv[3]
        print("ack for ",ack_num)
        if ack_num == first_in_window:
              
            lock.acquire()
            acked[first_in_window % N] = 0
            send_buffer[first_in_window % N] = None
            retrans[first_in_window % N] = 0
            
            num_acked = num_acked + 1
            
            first_in_window = first_in_window + 1
            first_in_window = int(first_in_window % ((2*N)))
            lock.release()
            
            it = first_in_window 
            while acked[it % N] == 1:
                lock.acquire()
                acked[it % N] = 0
                send_buffer[it % N] = None
                retrans[it % N] = 0
                
                num_acked = num_acked + 1
                first_in_window = first_in_window + 1
                first_in_window = int(first_in_window % ((2*N)))
                lock.release()

                it = first_in_window
        else:
            if first_in_window < last_in_window:
             if ack_num > first_in_window and ack_num <= last_in_window:
              acked[ack_num % N] = 1
            else:
             if (ack_num > first_in_window and ack_num < ((2*N))) or (ack_num >=0 and ack_num <= last_in_window):
              acked[ack_num % N] = 1

            
        if send_complete == 1 and num_acked >= total_acks:
            ack_complete = 1


def get_file(file_name):
    
    global seq_num
    global to_send
    global last_in_window
    global send_buffer
    global timeout_timers
    global TIMEOUT
    global send_complete
    global first_in_window
    global N
    global M
    global ack_complete
    global server_seq
    global client_seq
    global total_acks
    global max_retrans
    

    if os.path.isfile(file_name):
      
        pkt_number = 0
        file_size = os.stat(file_name).st_size 
        
        pkts = int(file_size / 3096)
        total_acks = pkts
        if file_size % 3096 !=0:
         pkts = pkts + 1
        
        fp = open(file_name, "rb")
        server_seq = 0
        seq=0
        count = 0
        while pkts != 0:
            to_send = last_in_window + 1
            
            data_string = encodeHeader(int('00010000',2),int('00000100',2),server_seq,int((client_seq+1)%(2*M)))
            data_string = data_string + fp.read(3096)
            
            if count < N:
                send_buffer.append(data_string)
                timeout_timers.append(time())
                retrans.append(1)
            else:
                send_buffer[to_send % N] = data_string
                timeout_timers[to_send % N] = time()
                retrans[to_send % N] = 1
            s.sendto(data_string, addr)
            count+=1
            server_seq = int((server_seq+1)%(2*N))
            seq = seq + 1
           
            pkt_number += 1
            pkts-=1
            if(pkts==0):
                send_complete=1
            
            last_in_window = last_in_window + 1
            last_in_window = int(last_in_window % (2*N))
            print("first_in_window ",first_in_window)
            print("last_in_window", last_in_window)
            
            if(first_in_window - last_in_window != 1):
             while(((last_in_window >= first_in_window ) and ((last_in_window - first_in_window) >= (N-1))) or ((last_in_window < first_in_window) and ((((2*N) - first_in_window + last_in_window + 1)) >= N))):
                if((first_in_window - last_in_window == 1) or (first_in_window == 0 and last_in_window == (2*N)-1 )):
                    break
                if ack_complete == 1:
                    break
                if(last_in_window >= first_in_window ):
                 it = first_in_window
                 while ((last_in_window >= first_in_window) and (it <= last_in_window) and ((last_in_window - first_in_window) >= (N-1))):
                    if((first_in_window - last_in_window == 1) or (first_in_window == 0 and last_in_window == (2*N)-1 )):
                     break
                    if (time() - timeout_timers[it % N]) >=TIMEOUT and send_buffer[it % N] != None:
                        
                        send_pkt = send_buffer[it % N]
                        if retrans[it % N] >= max_retrans:
                            s.close()
                            sys.exit()
                        s.sendto(send_pkt, addr)
                        retrans[it % N] = retrans[it % N] + 1
                        
                        sleep(0.1)
                        
                        timeout_timers[it % N] = time()
                    it = it + 1
                elif last_in_window < first_in_window :
                 it = first_in_window
                 while((last_in_window < first_in_window) and ((it >= first_in_window and it < (2*N)) or (it >= 0 and it <=last_in_window)) and ((((2*N) - first_in_window + last_in_window + 1)) >= N)):
                    if((first_in_window - last_in_window == 1) or (first_in_window == 0 and last_in_window == (2*N)-1 )):
                     break
                    print("first_in_window = ",first_in_window)
                    print("last_in_window = ",last_in_window)
                    if (time() - timeout_timers[it % N]) >=TIMEOUT and send_buffer[it % N] != None:
                        
                        send_pkt = send_buffer[it % N]
                        if retrans[it % N] >= max_retrans:
                            s.close()
                            sys.exit()
                        s.sendto(send_pkt, addr)
                        retrans[it % N] = retrans[it % N] + 1
                        sleep(0.1)
                        
                        timeout_timers[it % N] = time()
                    it = it + 1
                    if it == (2*N):
                     it = 0
                                  
        while ack_complete == 0:
            if(last_in_window >= first_in_window ):
                 it = first_in_window
                 while it <= last_in_window:
                    if ack_complete == 1:
                        break
                    if (time() - timeout_timers[it % N]) >=TIMEOUT and send_buffer[it % N] != None:
                       
                        send_pkt = send_buffer[it % N]
                        if retrans[it % N] >= max_retrans:
                            s.close()
                            sys.exit()
                        s.sendto(send_pkt, addr)
                        retrans[it % N] = retrans[it % N] + 1
                        
                        
                        timeout_timers[it % N] = time()
                    it = it + 1
                    it = it % (2*N)
            elif (last_in_window < first_in_window ):
                 it = first_in_window
                 while((it >= first_in_window and it < (2*N)) or (it >= 0 and it <=last_in_window)):
                    if ack_complete == 1:
                        break
                    if (time() - timeout_timers[it % N]) >=TIMEOUT and send_buffer[it % N] != None:
                        
                        send_pkt = send_buffer[it % N]
                        if retrans[it % N] >= max_retrans:
                            s.close()
                            sys.exit()
                        s.sendto(send_pkt, addr)
                        retrans[it % N] = retrans[it % N] + 1
                        
                        
                        timeout_timers[it % N] = time()
                    it = it + 1
                    it = it % (2*N)
             
        fp.close()
        

    else:
        msg = "Error: File does not exist in Server directory."
        print(msg)
        s.close()
        sys.exit()
        


hostname = ""

try:
    portnumber = int(sys.argv[1])
except:
    
    sys.exit()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lock = threading.Lock()
    
    s.bind((hostname, portnumber))
    
   
except socket.error:
    
    sys.exit()

### new syn
M=0
ret_timeout= TIMEOUT
cack_timeout= TIMEOUT
null_timeout= TIMEOUT
max_retrans=100
max_cack=10
connectionId=123

data, addr = s.recvfrom(4096)
print("recv ",data)
dv = getSynHeader(data)
temparr = BitArray(uint=dv[0], length=8)
synbit = bytes(temparr)[0]
flag=0
file_name = ""

getackdataThread = threading.Thread(target = getackdata, args = ())
getackdataThread.start()

if synbit == 1:
    server_seq = 0
    client_seq = dv[3]
    M= dv[5]
    while flag==0:
        data_string = encodeSynHeader(int('11000000',2),int('00010010',2),server_seq,int((client_seq+1)%(2*M)),int('10000000',2),N,ret_timeout,cack_timeout,null_timeout,max_retrans,max_cack,connectionId)
        s.sendto(data_string, addr)
        print("send ",data_string)
        server_seq = int((server_seq+1)%((2*N)))
        startTime = time()
        while(((time() - startTime)<=TIMEOUT) and (flag == 0)):
            pass



for i in range(N):
    acked.append(0)


first_in_window = 0

v = threading.Thread(target = getACKs, args = ())
v.start()
print(file_name)
get_file(file_name)


### new fin
sleep(5)
flagz=0
getackThread = threading.Thread(target = getack, args = ())
getackThread.start()
while flagz==0:
    data_string = encodeHeader(int('00100000',2),int('00000100',2),server_seq,client_seq)
    s.sendto(data_string, addr)
    print("fin send1 ",data_string )
    server_seq = int((server_seq + 1 ) % ((2*N)))
    startTime = time()
    while(((time() - startTime)<=TIMEOUT) and (flagz == 0)):
            pass
flagf=0
getfinThread = threading.Thread(target = getfin, args = ())
getfinThread.start()
while flagf==0:
    startTime = time()
    while(((time() - startTime)<=TIMEOUT) and (flagf == 0)):
            pass
data_string = encodeHeader(int('01000000',2),int('00000100',2),server_seq,client_seq)
print("fin send4 ",data_string )
s.sendto(data_string, addr)
client_seq = int((client_seq + 1 ) % ((2*N)))

sleep(5)
s.close()
sys.exit()

