import socket


bufferSize = 1024
worker0Address = "172.21.0.5"
# Port might be an issue
worker0Port = 50000

ingressIp = "172.21.0.2"

workerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
workerSocket.bind((worker0Address, worker0Port))

print("Worker up and listening!")

while(True):
    bytesAddressPair = workerSocket.recvfrom(bufferSize)
    
    nack = True
    messageToSend = "nack"

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # No clue if this syntax is correct
    if (message[:0] != b'1'):
        print("Incorrect Header details worker 0")
        
        # Have to remove the first byte somehow.
        filename = message.decode('UTF-8')

        if(filename == "file3.txt"):
            try:
                messageToSend = open(filename, 'r').readlines()
            except FileNotFoundError:
                messageToSend = "nack"
                print("Wrong file or file path")

    if (nack == True):
        print("Sending nack")
        msgBack = messageToSend
        workerSocket.sendto(address, msgBack.decode('UTF-8'))
    

