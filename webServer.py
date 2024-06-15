# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Listening for one connection at a time

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        
        try:
            # Receive the message from the client
            message = connectionSocket.recv(1024).decode()
            print(f"Message received: {message}")
            filename = message.split()[1]
            
            # Open the client requested file
            f = open(filename[1:], 'rb')
            outputdata = f.read()
            f.close()
            
            # Create a header for a valid response (200 OK)
            header = "HTTP/1.1 200 OK\r\n"
            header += "Server: MySimpleWebServer\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Connection: close\r\n"
            header += "\r\n"
            
            # Send the header
            connectionSocket.send(header.encode())
            
            # Send the body (file content)
            connectionSocket.send(outputdata)
            
            # Close the connection socket
            connectionSocket.close()
        
        except IOError:
            # Send response message for file not found (404)
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Server: MySimpleWebServer\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Connection: close\r\n"
            header += "\r\n"
            body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
            
            # Send the header and the body
            connectionSocket.send(header.encode())
            connectionSocket.send(body.encode())
            
            # Close the connection socket
            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
