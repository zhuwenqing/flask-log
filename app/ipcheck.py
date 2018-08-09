import socket
def getIP(doamin):
    myaddr=socket.getaddrinfo(doamin,'http')
    return myaddr[0][4][0]
    # print(myaddr[0][4][0])