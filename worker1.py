import socket


bufferSize = 1024
worker0Address = "172.21.0.4"
# Port might be an issue
worker0Port = 50000

ingressIp = "172.21.0.2"

workerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
workerSocket.bind((worker0Address, worker0Port))

print("Worker up and listening!")

while(True):
    bytesAddressPair = workerSocket.recvfrom(bufferSize)
    
    filename = ""
    nack = True
    messageToSend = "nack"

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # No clue if this syntax is correct

    if (message[0] != 49):
        print("Incorrect Header details worker 0")
        messageToSend = "nack"
        # Have to remove the first byte somehow.

    filename = message[1:].decode('UTF-8')
    if(filename == "file2.txt"):
        try:
            messageToSend = open(filename, 'r').readlines()
        except FileNotFoundError:
            messageToSend = "nack"
            print("Wrong file or file path")

    if (nack == True):
        print("Sending nack")
        msgBack = str(messageToSend)
        workerSocket.sendto(msgBack.encode('UTF-8'), address)
    

