import socket
import tqdm
import os

SEPARATOR = "<SEPERATOR>"
bufferSize = 1024



worker0Address = "172.21.0.3"
# Port might be an issue
worker0Port = 50000
fileHeader = b'1'
ingressIp = "172.21.0.2"

workerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
workerSocket.bind((worker0Address, worker0Port))

print("Worker up and listening!")

while(True):
    bytesAddressPair = workerSocket.recvfrom(bufferSize)
    
    filename = ""
    nack = True
    messageToSend = "file not found"

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # No clue if this syntax is correct

    if (message[0] != 49):
        print("Incorrect Header details worker 0")
        messageToSend = "nack"
        # Have to remove the first byte somehow.

    filename = message[1:].decode('UTF-8')
    if(filename == "file1.txt"):
        try:
            filesize = os.path.getsize(filename)
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    # Reads the bytes one at a time
                    bytes_read = f.read(bufferSize-1)
                    if not bytes_read:
                        break
                    bytesWithoutHeader = bytearray(bytes_read)
                    bytesWithoutHeader[:0] = fileHeader
                    bytesToSend = bytes(bytesWithoutHeader)
                    
                    workerSocket.sendto(bytesToSend, address)
                    progress.update(len(bytesToSend))
                    nack = False
        except FileNotFoundError:
            messageToSend = "file not found"
            print("Wrong file or file path")

    if (nack == True):
        print("Sending nack")
        msgBack = str(messageToSend)
        workerSocket.sendto(msgBack.encode('UTF-8'), address)
    

