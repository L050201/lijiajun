import socket
import sys
#Import the necessary Python libraries

def send_request(client_socket, request):
    message_size = str(len(request)).zfill(3)
    full_request = message_size + request
    client_socket.send(full_request.encode('utf - 8'))
    response = client_socket.recv(1024).decode('utf - 8')
    return response
#Function to send a request to the server and receive the response

