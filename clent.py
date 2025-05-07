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

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <request_file>")
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]
#A function called main is defined, which is the main function of the client program, which is mainly responsible for handling command-line arguments, verifying the number of arguments, and extracting the required information from the command line
