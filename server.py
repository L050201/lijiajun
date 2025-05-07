import socket
import threading
import time
# create a socket object

class TupleSpace:
    def __init__(self):
        self.tuples = {}
        self.client_count = 0
        self.operation_count = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.error_count = 0
        #A tuple space is initialized, and initial values are assigned to properties that record the number of client connections, the total number of operations, the number of different operations, and the number of errors, which can be used to later count and monitor the operations of the tuple space
    
    def put(self, key, value):
        if key in self.tuples:
            self.error_count += 1
            return 1
        self.tuples[key] = value
        self.put_count += 1
        return 0    
    #Inserts a new key-value pair into the tuple space

    def read(self, key):
        if key not in self.tuples:
            self.error_count += 1
            return ""
        self.read_count += 1
        return self.tuples[key]
    #Reads the value of the specified key from the tuple space

    def get(self, key):
        if key not in self.tuples:
            self.error_count += 1
            return ""
        value = self.tuples.pop(key)
        self.get_count += 1
        return value
    #Removes the key-value pair with the specified key from the tuple space and returns its value

    def print_summary(self):
        tuple_count = len(self.tuples)
        if tuple_count == 0:
            avg_tuple_size = 0
            avg_key_size = 0
            avg_value_size = 0
        else:
            total_tuple_size = sum(len(key) + len(value) for key, value in self.tuples.items())
            total_key_size = sum(len(key) for key in self.tuples.keys())
            total_value_size = sum(len(value) for value in self.tuples.values())
            avg_tuple_size = total_tuple_size / tuple_count
            avg_key_size = total_key_size / tuple_count
            avg_value_size = total_value_size / tuple_count
            #Prints statistics for the tuple space, including the number of tuples, the average tuple size, the average key size, the average size, as well as the number of clients, the total number of operations, the number of executions of different operations, and the number of errors
        print(f"Tuple Space Summary - "
              f"Tuples: {tuple_count}, "
              f"Avg Tuple Size: {avg_tuple_size}, "
              f"Avg Key Size: {avg_key_size}, "
              f"Avg Value Size: {avg_value_size}, "
              f"Total Clients: {self.client_count}, "
              f"Total Operations: {self.operation_count}, "
              f"Total READs: {self.read_count}, "
              f"Total GETs: {self.get_count}, "
              f"Total PUTs: {self.put_count}, "
              f"Total Errors: {self.error_count}")
        #Prints the summary in a formatted way



    def handle_client(client_socket, tuple_space):
       tuple_space.client_count += 1
       try:
           while True:
                data = client_socket.recv(1024).decode('utf - 8')
                if not data:
                  break
                message_size = int(data[:3])
                command = data[3]
                key = data[4:message_size - 1] if command != 'P' else data[4:message_size - len(data.split(' ')[-1]) - 2]
                value = data.split(' ')[-1] if command == 'P' else ""
                tuple_space.operation_count += 1
                response = ""   
                #Client connection counting, continuous receipt of client data, parsing data, and operation counting are done
                if command == 'R':
                    result = tuple_space.read(key)
                    if result:
                        response = f"{str(len(f'OK ({key}, {result}) read')).zfill(3)} OK ({key}, {result}) read"
                    else:
                       response = f"{str(len(f'ERR {key} does not exist')).zfill(3)} ERR {key} does not exist"
                elif command == 'G':
                    result = tuple_space.get(key)
                    if result:
                        response = f"{str(len(f'OK ({key}, {result}) removed')).zfill(3)} OK ({key}, {result}) removed"
                    else:
                        response = f"{str(len(f'ERR {key} does not exist')).zfill(3)} ERR {key} does not exist"
                elif command == 'P':
                    result = tuple_space.put(key, value)
                    if result == 0:
                         response = f"{str(len(f'OK ({key}, {value}) added')).zfill(3)} OK ({key}, {value}) added"
                    else:
                         response = f"{str(len(f'ERR {key} already exists')).zfill(3)} ERR {key} already exists"
                client_socket.send(response.encode('utf - 8'))
       finally:
        client_socket.close()
        #Perform an operation on the tuple space based on the command received from the client, and send the result back to the client in a response message in a specific format
        