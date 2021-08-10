Info about terminologies in context of our implementation :
1. Server is the file sender.
2. Client is the file receiver.
3. server.py and client.py are protocol files and serverapp.py and clientapp.py are application implementation files.

Instructions to compile and run :
1. In clientapp.py change "DESKTOP-AJ2KI5T" to the hostname of the client system and change "5500" to the port you want to use.
2. In serverapp.py change "5500" to the port you want to use.
3. Run serverapp.py as " python3 serverapp.py".
4. Run clientapp.py as "python3 clientapp.py", it will ask for filename you want to receive.
5. Enter input as "get file.txt", if you want to get file.txt from server.py
6. File transfer will begin with 3-way handshake synchronization and end after connection close process.
7. Program might stop for a few seconds somewhere since sleep() was used to avoid overloading the udp socket. It will resume again.
8. After file transfer both serverapp.py and clientapp.py will exit.
9. To transfer another file, begin from step 1 again.

Changes to protocol :

1. In "Connection setup" section, initial sequence numbers are chosen as 0 instead of a random number.

2. "Connection close" section is updated as below:
 {
  Connection close :
  1. Server initiates closing of the connection by sending a packet with FIN bit set and sequence
  number at that time(say x). Server enters FIN_WAIT_1 state.
  2. Client on receiving the previous packet, send a packet with ACK bit set and ACKnum at that
  time(say y). Client enters CLOSE_WAIT state.
  3. Server on receiving, enters FIN_WAIT_2 state.
  4. Client sends a packet with FIN bit set and sequence number y and enters LAST_ACK state.
  5. On receiving, Server sends a packet with ACK bit set and ACKnum as y+1 and enters
  TIMED_WAIT state and after a timed wait, enters CLOSED state.
  6. Client enters CLOSED state on receiving the packet.
  Connection is closed.
 }