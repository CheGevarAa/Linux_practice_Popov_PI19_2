import socket 
import select 
import sys 
  
main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print ("Your input must be: script, IP-address, port number")
    exit()
    
host = str(sys.argv[1]) 
port = int(sys.argv[2]) 
main_sock.connect((host, port)) 
  
while True: 
    
    sockets_list = [sys.stdin, main_sock] 

    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for sock in read_sockets:
        if sock == main_sock:
            msg = sock.recv(2048) 
            print(msg) 
        else: 
            msg = sys.stdin.readline()
            main_sock.send(msg) 
            sys.stdout.write("<You>") 
            sys.stdout.write(msg) 
            sys.stdout.flush() 
main_sock.close() 