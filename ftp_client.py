import socket
HOST = 'localhost'
PORT = 8000

requests = ['GET /connect/UserOne/12345', 'GET /pwd/', 'GET /mkdir/myfolder', 'GET /ls/', 'GET /rename/myfolder//documents',
            'GET /rmdir/myfolder', 'GET /rmfile/', 'GET /toclient/documents/text.txt', 'GET /disconnect/']

for request in requests:
    sock = socket.socket()
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(e)
    print(request)
    sock.send(request.encode())
    response = sock.recv(8192).decode()
    if response == 'error':
        print('Error in ' + request)
    else:
        print(response)

    sock.close()
