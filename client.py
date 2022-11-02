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
    print(serverAddressPort)
    print(bytesToSend)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    count = 0
    # Stop and Wait ARQ
    while True:
        count = count + 1
        # Asking the user what file it would like to send    
        try:
            UDPClientSocket.settimeout(10)
            with open(str(count) + ".txt", "wb") as f:
                while True:
                    bytes_read = UDPClientSocket.recvfrom(bufferSize)
                    if not bytes_read:
                        break
                    bytesMsg = bytes_read[0]
                    if(bytesMsg == b'file not found'):
                        print("File has not been found")
                        ack= "1"
                        break

                    bytesToWrite = bytesMsg[1:]                    
                    f.write(bytesToWrite)
                    ack = "1"
                f.close
        except socket.timeout:
            while(ack_positive != ack):
                print("Resending ack")
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)   
                break
        if(ack_positive == ack):
            break
        # Acknowledgement recieved and parsing data




