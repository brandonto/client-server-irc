"""
Trial project - Team NILE
IRC chat server
"""

import socket, select, re, fcntl, struct

"""
http://raspberrypi.stackexchange.com/questions/6714/how-to-get-the-raspberry-pis-ip-address-for-ssh
"""
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24]
    )
    #usage: get_ip_address('lo')
    #       get_ip_address('eth0')

#"""
#Get username according to IP address
#"""
#def userName(address):
#    ipAddress = re.search('\'[\d]*.[\d]*.[\d]*.[\d]*\'', address).group(0).strip('\'')
#    if ipAddress == "10.0.0.21":
#	    return "Noah"
#    elif ipAddress == "10.0.0.22":
#	    return "Brandon"
#    elif ipAddress == "10.0.0.23":
#	    return "Nhat"
#    elif ipAddress == "10.0.0.24":
#	    return "Haifa"
#    elif ipAddress == "10.0.0.25":
#	    return "Itaf"
#    elif ipAddress == "192.168.1.10":
#	    return "Desktop"
#    else:
#	    return address

"""
Send data to clients in socket list
Except for the client who sent the data
"""
def sendData(sock, message):
    for socket in CLIENTS_LIST:
	if socket != listeningSocket and socket != sock:
	    try:
		    socket.send(message)
	    except:
		    socket.close()
		    CLIENTS_LIST.remove(socket)

"""
Get message from 1 client and send it across all other clients and close disconnected clients"
"""
def runChatProgram():
    while True:
	read_sockets,write_sockets,error_sockets = select.select(CLIENTS_LIST, [], [])
	for clientSocket in read_sockets:
	    """
	    Spawn new listening socket to client connection and send out notice
	    """
	    if clientSocket == listeningSocket:
		    newClient, address = listeningSocket.accept()
		    CLIENTS_LIST.append(newClient)
		    #print userName(str(newClient.getpeername())) + " is connected\n"
		    print "A client has connected"
		    sendData(newClient, '<data><message sender="" payload="A new user has joined the chat room"></message></data>')
	    else:
		    try:
		        data = clientSocket.recv(BUFFER)
		        if data:
			        #sendData(clientSocket, '<' + userName(str(clientSocket.getpeername())) + '> ' + data)
			        sendData(clientSocket, data)
		    except:
		        #sendData(clientSocket, userName(str(clientSocket.getpeername())) + " left chat room")
		        #clientSocket.close()
		        #CLIENTS_LIST.remove(clientSocket)
		        continue

"""
 Main program, which opens server listening socket
 Listen to message comes from client and send it to other clients
"""
if __name__ == "__main__":

    # List of clients
    CLIENTS_LIST=[]
    # Buffer receive string
    BUFFER = 8192
    # Port which is listening to TCP connection
    PORT = 5000
    HOST = ""

    # Set up listen Socket
    listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSocket.bind((HOST, PORT))
    listeningSocket.listen(5)

    CLIENTS_LIST.append(listeningSocket)
    #print "Server is listening at static address: 10.0.0.1:" + str(PORT)
    print "Server is listening at static address: " + get_ip_address('eth0') + ":" + str(PORT)

    runChatProgram()
    listeningSocket.shutdown(SHUT_RDWR)

