#!/usr/bin/python

import socket
import sys
import threading

host = ''
port = 10101
BACKLOG = 5
buff_size = 128

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn_sock.bind((host, port))
conn_sock.listen(BACKLOG)

class EchoThread(threading.Thread):

    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.ip, self.port = address
        self.csocket = socket
        print("[+] New service thread started for {}" .format(self.ip))

    def run(self):
        data = self.csocket.makefile('r')
        request = data.readline()

        if request:
            command, filename = request.split()
        else:
            command = "void"

        if command == "get":
            try:
                fd = open(filename, 'r')
                result = '1'
            except:
                result = '0'

            if result == '1':
                response = 'Complete'+ '\n'

                self.csocket.sendall(response.encode())
                content = fd.read()
                self.csocket.sendall(content.encode())
                fd.close()
                data.close()

            elif result == '0':
                response = 'Fail' + '\n'
                self.csocket.sendall(response.encode())
                data.close()

            else:
                pass

        elif command == 'put':
            data.readline()

            fd = open(filename, 'w')
            rdata = data.readline()

            while rdata:
                fd.write(data)
                rdata = data.readline()

            fd.close()
            data.close()

        else:
            pass

        self.csocket.close()
        print("[-] Service thread terminated for {} ".format(self.ip))


while True:
    print("listening for incoming requests...")
    data_sock, client_address = conn_sock.accept()
    serviceThread = EchoThread(data_sock, client_address)
    serviceThread.setDaemon(True)
    serviceThread.start()