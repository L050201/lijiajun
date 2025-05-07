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
