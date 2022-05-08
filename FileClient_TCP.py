#!/usr/bin/python3
import socket
import sys

host = '203.250.133.193'
port = 10101

while True :
    req = input("vsftp> ")
    req_field = req.split()

    if len(req_field) == 1 :
        command = req_field[0]
    elif len(req_field) == 2 :
        command = req_field[0]
        filename = req_field[1]
    else :
        continue

    if len(req_field) == 1 :
        if command.upper() == 'QUIT':
            break
        else :
            print("Unknown Command... ")
            continue

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        sock.connect(server_address)
    except:
        print("connection failed...")
        sys.exit(0)

    if command.upper() == 'GET' :
        message = command + ' ' + filename + '\n'
        sock.sendall(message.encode())

        data = sock.makefile('r')
        response = data.readline()
        result, phrase = response.split()

        if result == '1' :
            data.readline()
            fd = open(filename, 'w')
            rdata = data.readline()
            while rdata:
                fd.write(data)
                rdata = data.readline()

            print("File Download Completed")
            fd.close()
            sd.close()

        elif result == '0' :
            print("File Not Found")
        else :
            pass

    elif command.upper() == 'PUT':

        d_read = sock.makefile("r")
        d_write = sock.makefile("w")

        req_line = "PUT" + filename + "\n"

        fd = open(filename, "r")
        content = fd.read()

        d_write.write(req_line)
        d_write.write(body)

        print("File Upload Completed")
        d_write.close()
        fd.close()
        d_read.close()
    else :
        pass

    sock.close()
