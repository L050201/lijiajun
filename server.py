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