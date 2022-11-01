import socket

worker0Address = "172.21.0.3"
worker1Address = "172.21.0.4"
worker2Address = "172.21.0.5"


internalIp = "172.21.0.2"
externalIp = "172.20.0.2"

# Another thing to check is if the two different ports affect anything
workerPorts = 50000
externalPort = 50000
internalPort = 50001
bufferSize = 1024
count = 1

# Create a datagram socket
UDPServerSocketExternal = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
UDPServerSocketInternal = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocketInternal.bind((internalIp, internalPort))
UDPServerSocketExternal.bind((externalIp, externalPort))
print("UDP Server up and listening!")

while(True):
    print("Waiting for message")
    bytesAddressPair = UDPServerSocketExternal.recvfrom(bufferSize)
    print(externalIp)
    print("Got a message!")
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print("Its from")
    print(address)  
    print(message)  
    fileContents = "";

    # Things to be noted it will check each one of the workers regardless of a positive outcome or not
    # Need to implement some kind of loop so that we can send larger files

    # Send a message to all workers
    # Send to worker 1
    UDPServerSocketInternal.sendto(message, (worker0Address, workerPorts))
    bytesIntAddressPair = UDPServerSocketInternal.recvfrom(bufferSize)
    messageInt = bytesIntAddressPair[0]
    addressInt = bytesIntAddressPair[1]
    
    if (messageInt.decode('UTF-8') != "nack"):
        fileContents = messageInt.decode('UTF-8')
        #Probably something valid got sent      

    # Send to worker 2
    UDPServerSocketInternal.sendto(message, (worker1Address, workerPorts))
    bytesIntAddressPair = UDPServerSocketInternal.recvfrom(bufferSize)
    messageInt = bytesIntAddressPair[0]
    addressInt = bytesIntAddressPair[1]
    
    if (messageInt.decode('UTF-8') != "nack"):
        fileContents = messageInt.decode('UTF-8')
    
    # Send to worker 3
    UDPServerSocketInternal.sendto(message, (worker2Address, workerPorts))
    bytesIntAddressPair = UDPServerSocketInternal.recvfrom(bufferSize)
    messageInt = bytesIntAddressPair[0]
    addressInt = bytesIntAddressPair[1]
    
    if (messageInt.decode('UTF-8') != "nack"):
        fileContents = messageInt.decode('UTF-8')

    # Message to powershell
    # This just sends back the file contents back to the address (Client)    
    clientMsg = "The client would like file :{} ".format(message)
    clientIP = "Client IP Address:{}".format(address)
    
    print("Here you guy my man, enjoy this!")
    UDPServerSocketInternal.sendto((fileContents, address))
    

    
    
            


