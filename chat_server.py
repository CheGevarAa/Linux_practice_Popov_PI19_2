import socket 
import select 
import sys 
from thread import *
from random import choice, randint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
if len(sys.argv) != 3: 
    print ("Your input must be: script, IP-address, port number")
    exit() 

host = str(sys.argv[1]) 
port = int(sys.argv[2]) 
  
sock.bind((host, port)) 
sock.listen(50) 
global clients  
clients = {} 

nicknames = ['frog', 'banana', 'smol', 'deadly AI', 'milky way', 'carrot', 'potato', 'math addicted', 'ctrlaltdel']
  
class Client_thread: 
    def __init__(self, conn):
    	self.conn = conn
	self.main()

    def main(self):

  	 self.conn.send("Welcome to the chatroom!\n")
	 self.conn.send("Users: " + str(clients.values()))
  
   	 while True: 
           	 try: 
                	msg = self.conn.recv(2048)
                	if msg:
                   		 msg_to_send = "<" + clients[self.conn] + ">: " + msg 
                   		 print(msg_to_send) 
                   		 for client in clients.keys():
                			if client!=self.conn: 
                        			try: 
                                			client.send(msg_to_send) 
                        			except: 
                                			client.close() 
                                			if conn in clients.getkeys(): 
                                        			clients.pop(conn) 
  
                	else: 
                    		self.remove(self.conn) 
            	 except: 
                	continue


    def remove(connection): 
   	 if connection in clients.getkeys(): 
        	clients.pop(connection) 


def main():
    while True: 
  
        conn, addr = sock.accept() 
  
        clients[conn]=choice(nicknames)+str(randint(1, 50))  
        print (addr[0], clients[conn] + " connected")
	print(clients)	
        start_new_thread(Client_thread,(conn,))     
  
    conn.close() 
    sock.close()
    
if __name__ == '__main__':
    main()