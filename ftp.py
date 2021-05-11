import socket
import os


def process(req):
    global users
    user = users[0]
    homedir = '/home/anna-beng/PycharmProjects/FTP/workspace/'
    if req.startswith('GET /pwd/'):
        with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - pwd\n')
        return str(os.getcwd())+'/workspace'
    elif req.startswith('GET /ls/'):
        folder_name = req.split()[1][4:]
        with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - ls\n')
        if folder_name:
            return ', '.join(os.listdir(homedir+folder_name))
        else:
            return ', '.join(os.listdir(homedir))
    elif req.startswith('GET /mkdir/'):
        folder_name = req.split()[1][7:]
        try:
            os.mkdir(homedir + folder_name)
            with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
                log.write(user + ' - mkdir '+folder_name+'\n')
            return 'Folder created'
        except OSError:
            return 'Error'
    elif req.startswith('GET /rmdir/'):
        folder_name = req.split()[1][7:]
        try:
            response = rmdir(homedir + folder_name)
            if response != 'error':
                with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
                    log.write(user + ' - rmdir ' + folder_name+'\n')
            return response
        except OSError:
            return 'Error'
    elif req.startswith('GET /rmfile/'):
        file_name = req.split()[1][8:]
        try:
            os.remove(homedir + file_name)
            with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
                log.write(user + ' - rmfile ' + file_name+'\n')
            return 'File deleted'
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /rename/'):
        data = req.split()[1][8:]
        old = data.split('//')[0]
        new = data.split('//')[1]
        try:
            os.rename(homedir + old, homedir + new)
            with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
                log.write(user + ' - rename ' + new+'\n')
            return 'File renamed'
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /toclient/'):
        data = req.split()[1][10:]
        try:
            with open(homedir+data, 'r') as file:
                    with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
                        log.write(user + ' - copied from server ' + data+'\n')
                    return file.read()
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /disconnect/'):
        with open('/home/anna-beng/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - disconnect\n')
        return 'Close connection'
    else:
        return 'Bad request'


def rmdir(path):
    if not os.listdir(path):
        try:
            os.rmdir(path)
            return 'Folder deleted'
        except OSError:
            return 'Error'
    else:
        try:
            for file in os.listdir(path):
                os.remove(path + '/' + file)
            os.rmdir(path)
            return 'Folder deleted'
        except:
            return 'Error'



SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s...' % SERVER_PORT)
users = ['Admin']


while True:
    conn, addr = server_socket.accept()
    request = conn.recv(8192).decode()
    print(request)
    content = process(request)
    print(content)
    response = """HTTP/1.1 200 OK
                Server: SelfMadeServer v0.0.1
                Content-type: text/html
                Connection: close\n\n""" + content
    conn.sendall(response.encode())
    if request.startswith('GET /disconnect/'):
        conn.close()
        break

server_socket.close()
