import socket
log = open("ServerLog.txt", "a")
clients = open("Clients.txt", "a+")
log.write('Server starting...\n')
sock = socket.socket()
port=input("Type in the port: ")
try:
	if not ((0<=port<65536) and isinstance(port, int)):
		log.write('Wrong port id, the default one will be used (9080)\n')
		print('Wrong port id, the default one will be used (9080)\n')
		port=9080
	sock.bind(('', int(port)))
except (socket.error):
	print('this port is busy, redirecting to 65000...\n')
	sock.bind(('', 65000))
while True:
	log.write('Listening to the port: ' + str(port) + "\n")
	sock.listen(1)
	conn, addr = sock.accept()
	log.write('Connected to ' + addr[0] + ' ' + str(addr[1]) + '\n')
	print('Connected to ' + addr[0] + ' ' + str(addr[1]))
	for i in clients:
		if addr[0] in i:
			print('Hello, ' + str(i.split(':')[1]))
			break
	else:
		name=input('Type in your name please: \n')
		clients.write(str(addr[0]+':'+name+'\n'))
	while True:
		msg = ''
		data = conn.recv(1024)
		if not data:
			break
		log.write('Accepting data...\n')
		msg += data.decode()
		log.write(msg + '\n')
		log.write('Sending data...\n')
		conn.send(data)
		print(msg)

	log.write('Closing connection...\n')
	conn.close()
log.close()
clients.close()