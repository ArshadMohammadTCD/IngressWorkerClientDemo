import socket

serverAddressPort = ("172.20.0.2", 50000)
bufferSize = 1024
fileHeader = b'1'

print("Server address port is ")
print(serverAddressPort)

ack_positive = "1";
ack = "0";

print("Creating UDP Client Socket..")
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("UDP Client socket made")

while True:
    msgFromClient = input("Name what file you would like: \n")
    bytesWithoutHeader = bytearray(str.encode(msgFromClient))
    bytesWithoutHeader[:0] = fileHeader
    bytesToSend = bytes(bytesWithoutHeader)
    print("Sending this to ")
    print(bytesToSend)

    count = 0
    # Stop and Wait ARQ
    while True:
        count = count + 1
        # Asking the user what file it would like to send    
        try:
            UDPClientSocket.settimeout(10)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)
            fileWrite = msgFromServer[0].decode('UTF-8')
            ack = "1"
            f = open(str(count), "x")
            f.write(fileWrite)
            f.close
        except socket.timeout:
            while(ack_positive != ack):
                print("Resending ack")   
                break
        
        if(ack_positive == ack):
            break
        # Acknowledgement recieved and parsing data




