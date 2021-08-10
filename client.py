#ACHYUTA KRISHNA V - 2018A7PS0165H
#ANIRUDH G - 2018A7PS0217H
#AJITH P J - 2018A7PS0040H
#J ALVIN RONNIE - 2018A7PS0029H
#MANEESH REDDY - 2018A7PS0462H

import pickle
#from socket import gethostbyname
from socket import *
import random
from time import time
from time import sleep
import os
import sys
#from packet import Packet
import bitstring
from bitstring import BitArray
from struct import *
import threading

totalbytes = 0
startt = 0
clientAddress = ('0',0)
flag = 0
z = 0
def getack():
    global flagz
    if flagz==1:
        return
    recv_pkt, serverAddress = s.recvfrom(4096)
    dv = getHeader(recv_pkt)
    temparr = BitArray(uint=dv[0], length=8)
    ackbit = bytes(temparr)[1]
    if ackbit==1:
        flagz=1
        return

def syngetack():
    global flag
    global server_seq
    global client_seq
    global M
    global clientAddress
    if flag == 1:
        return;
    recv_pkt, serverAddress = s.recvfrom(4096)
    clientAddress = serverAddress
    print("recv ",recv_pkt)
    if recv_pkt == -1:
        return
    dv = getSynHeader(recv_pkt)
    temparr = BitArray(uint=dv[0], length=8)
    synbit = bytes(temparr)[0]
    ackbit = bytes(temparr)[1]
    if ((ackbit == 1) and (synbit == 1)):
        server_seq = dv[2]
        client_seq = dv[3]
        M = dv[5]
        flag = 1
        return
def dataget():
    global datapkt
    global z
    if z == 1:
        return
    recv_pkt, serverAddress = s.recvfrom(4096)
    #print("recv ",recv_pkt)
    dv = getHeader(recv_pkt)
    if(dv == None):
        return
    temparr = BitArray(uint=dv[0], length=8)
    databit = bytes(temparr)[3]
    if databit == 1:
        datapkt = recv_pkt
        z=1
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
    while(i<len(header)):
     ans.append(ord(header[i]))
     i+=1
    return ans

def getData(pkt):
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


# python3 client.py hostname portnumber windowsize
c=0
server_seq=0
server_acknum=0
client_seq=0
client_acknum=0
try:
    gethostbyname(sys.argv[1])
except socket.error:
    print("Invalid host name.")
    sys.exit()

hostname = sys.argv[1]
try:
    portnumber = int(sys.argv[2])
except:
    print("Invalid port number")
    sys.exit()

N = int(sys.argv[3]) #window size
loss = -0.5

try:
    s = socket(AF_INET, SOCK_DGRAM)
    print("Client socket initialized")
    s.setblocking(0)
    s.settimeout(1500)
except socket.error:
    print("Failed to create socket")
    sys.exit()

def ack(sequenceNo, clientAddress):
    global client_seq
    global N
    try:
        #p = Packet(False,True,False,True,False,0,client_seq,sequenceNo)
        ackseg = encodeHeader(int('01000000',2),int('00000100',2),client_seq,sequenceNo)
        #data_string = pickle.dumps(p)
        s.sendto(ackseg, (hostname, portnumber))
        client_seq = int((client_seq + 1 ) % ((2*N)))
        print("sending ack for seq = ",sequenceNo)
    except ConnectionResetError:
        print("Error")
        sys.exit()

last_recvd = -1
seq = 0

received = [] #int buffer to indicate if packet has been received
recv_buffer = [] #buffer to store the received packets
first_in_window = 0
last_in_window = first_in_window + N - 1

for i in range(N):
    received.append(0)
    recv_buffer.append(None)


command = input("Please enter the command as: get [file_name]\n")
cmd = command.split() 
encoded_command = cmd[1].encode('utf8')
#### new syn
TIMEOUT = 1
M = 0
ret_timeout=2
cack_timeout=3
null_timeout=1
max_retrans=10
max_cack=10
connectionId=123
client_seq = 0

syngetackThread = threading.Thread(target = syngetack, args = ())
syngetackThread.start()
while flag == 0:
    synseg = encodeSynHeader (int('10000000',2),int('00010010',2),client_seq,0,int('10000000',2),N,ret_timeout,cack_timeout,null_timeout,max_retrans,max_cack,connectionId)
    print("send",synseg)
    s.sendto(synseg, (hostname, portnumber))
    client_seq = int((client_seq + 1 ) % ((2*N)))
    startTime = time()
    while((time() - startTime <= TIMEOUT) and (flag == 0)):
        pass

#at this point synbit sent and syn ack received

datagetThread = threading.Thread(target = dataget, args = ())
datagetThread.start() 
while z == 0:
    data_string = encodeHeader(int('01010000',2),int('00000100',2),client_seq,int((server_seq+1) % (2*M)))
    data_string = data_string + encoded_command
    print(encoded_command)
    print("send",data_string)
    s.sendto(data_string, clientAddress)
    
    client_seq = int((client_seq + 1 ) % ((2*N)))
    startTime = time()
    while((time() - startTime <= 10) and (z == 0)):
        pass


if cmd[0] == "get":
    
    fp = open("Received-" + cmd[1], "wb")

    print("Receiving packets...")
    startt = time()
    seq=0
    #prev=-1
    while 1:
       data, clientAddress = s.recvfrom(4096)
       header = getHeader(data)
       temparr = BitArray(uint=header[0], length=8)
       finbit = bytes(temparr)[2]
       print("finbit = ",finbit)
       if finbit == 1:
        print(time() - startt)
        server_seq = header[2]
        print("fin data",data)
        fp.close()
        break

       if random.random() > loss :  
        
        file_data = getData(data)
        seq = header[2]
        
        if first_in_window < last_in_window :
         if seq < first_in_window:
                
            ack(seq, clientAddress)

         elif seq >= first_in_window and seq <= last_in_window:
                

            if seq == first_in_window:
                   
                fp.write(file_data)
                totalbytes = totalbytes + len(file_data)
                recv_buffer[first_in_window % N] = None
                received[first_in_window % N] = 0
                first_in_window = first_in_window + 1
                first_in_window = int(first_in_window % (2*N) )
                last_in_window = last_in_window + 1
                last_in_window = int(last_in_window % (2*N) )
                it = first_in_window
                while received[it % N] == 1:
                    fp.write(recv_buffer[it % N])
                    
                    recv_buffer[it % N] = None
                    received[it % N] = 0
                    first_in_window = first_in_window + 1
                    first_in_window = int(first_in_window % (2*N) )
                    last_in_window = last_in_window + 1
                    last_in_window = int(last_in_window % (2*N) )
                    it = first_in_window

            elif received[seq % N] == 0:
                recv_buffer[seq % N] = file_data
                received[seq % N] = 1

               
            ack(seq, clientAddress)
        else:
         if seq < first_in_window and seq > last_in_window :
            ack(seq, clientAddress)
         elif (seq >= first_in_window and seq <(2*N) ) or (seq >= 0 and seq <= last_in_window):

            if seq == first_in_window:
                    
                fp.write(file_data)
                
                recv_buffer[first_in_window % N] = None
                received[first_in_window % N] = 0
                first_in_window = first_in_window + 1
                first_in_window = int(first_in_window % (2*N) )
                last_in_window = last_in_window + 1
                last_in_window = int(last_in_window % (2*N) )
                it = first_in_window
                while received[it % N] == 1:
                    fp.write(recv_buffer[it % N])
                    
                    recv_buffer[it % N] = None
                    received[it % N] = 0
                    
                    first_in_window = first_in_window + 1
                    first_in_window = int(first_in_window % (2*N) )
                    last_in_window = last_in_window + 1
                    last_in_window = int(last_in_window % (2*N) )
                    it = first_in_window

            elif received[seq % N] == 0:
                    
                recv_buffer[seq % N] = file_data
                received[seq % N] = 1

                #ACK the packet
            ack(seq, clientAddress)

    fp.close()
    print("File received")
elif cmd[0] == "exit":
    s.close()
    sys.exit()

print("File received")

### new fin
flagz=0
getackThread = threading.Thread(target = getack, args = ())
getackThread.start()
retrans_count=0
endtimeout = time()
while flagz==0:
    data_string = encodeHeader(int('01000000',2),int('00000100',2),client_seq,server_seq)
    print("fin send2 ",data_string )
    s.sendto(data_string, (hostname, portnumber))
    client_seq = int((client_seq + 1 ) % ((2*N)))
    sleep(5)
    data_string = encodeHeader(int('00100000',2),int('00000100',2),client_seq,server_seq)
    s.sendto(data_string, (hostname, portnumber))
    print("fin send3 ",data_string )
    client_seq = int((client_seq + 1 ) % ((2*N)))
    startTime = time()
    retrans_count = retrans_count + 1
    if(time() - endtimeout >= 10):
        print('exit')
        flagz=1
        lock.release()
        s.close()
        sys.exit()
    if retrans_count > max_retrans:
        break;
    while(((time() - startTime)<=TIMEOUT) and (flagz == 0)):
        pass
s.close()
sys.exit()
