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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))
    #Create a client socket based on IPv4 and TCP protocols and use that socket to attempt to connect to the server on the specified host and port

    try:
        with open(request_file, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' ')
                command = parts[0]
                key = parts[1]
                value = parts[2] if len(parts) == 3 else ""
                if len(f"{key} {value}") > 970:
                    print(f"Error: Collated size of key and value exceeds 970 characters for {line}")
                    continue
                request = f"{command[0]} {key}"
                if command[0] == 'P':
                    request += f" {value}"
                response = send_request(client_socket, request)
                print(f"{line}: {response}")
                #Read each line in a given file, parse it into commands, keys, and values, construct a request and send it to the server, handle any possible key-value length exceeding the limit, and print the request and the corresponding server response