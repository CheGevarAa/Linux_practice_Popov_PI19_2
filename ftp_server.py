import socket
import os

def process(req):
    global user
    if request.startswith('GET /connect/'): #обработка запроса на получение информации
        print(users)
        login_data = req.split()[1][9:]
        login = login_data.split('/')[0]
        password = login_data.split('/')[1]
        if login in users.keys() and users[login] == password:
            with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
                log.write(login + ' - logged in\n')
                user = login
        else:
            user = None
            return "Authorization failed"
        return 'You have successfully logged in as ' + user

    if req.startswith('GET /register/'): #обработка запроса на получение информации
        login = req.split()[1][10:].split('/')[0]
        password = req.split()[1][10:].split('/')[1]
        if login not in users.keys():
            users[login] = password
            os.mkdir('/home/popov/PycharmProjects/FTP/workspace/' + login)
            with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
                log.write(login + ' - register\n')
            return 'You have registered successfully'
        else:
            return 'Such user exists'

    if not user: #проверка авторизации
        return 'Authorization needed'
    homedir = '/home/popov/PycharmProjects/FTP/workspace/' + user + '/'

    if req.startswith('GET /pwd/'): #обработка запроса на получение информации
        with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - pwd\n')
        return str('workspace/'+user)
    elif req.startswith('GET /ls/'): #обработка запроса 
        folder_name = req.split()[1][4:]
        with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - ls\n')
        if folder_name:
            return ', '.join(os.listdir(homedir+folder_name))
        else:
            return ', '.join(os.listdir(homedir))
    elif req.startswith('GET /mkdir/'): #обработка запроса
        folder_name = req.split()[1][7:]
        try:
            os.mkdir(homedir + folder_name)
            with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log: #запись в лог файл
                log.write(user + ' - mkdir '+folder_name+'\n')
            return 'Folder created: ' + homedir + folder_name
        except OSError:
            return 'Error'
    elif req.startswith('GET /rmdir/'):
        folder_name = req.split()[1][7:]
        try:
            response = rmdir(homedir + folder_name)
            if response != 'error':#обработка ошибки
                with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
                    log.write(user + ' - rmdir ' + folder_name+'\n')
            return response
        except OSError:
            return 'Error'
    elif req.startswith('GET /rmfile/'): #обработка запроса
        file_name = req.split()[1][8:]
        try:
            os.remove(homedir + file_name)
            with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log: #запись в лог файл
                log.write(user + ' - rmfile ' + file_name+'\n')
            return 'File deleted'
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /rename/'): #обработка запроса 
        data = req.split()[1][8:]
        old = data.split('//')[0]
        new = data.split('//')[1]
        try:
            os.rename(homedir + old, homedir + new)
            with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log: #запись в лог файл
                log.write(user + ' - rename ' + new+'\n')
            return 'File renamed'
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /toclient/'):#обработка запроса 
        data = req.split()[1][10:]
        try:
            with open(homedir+data, 'r') as file: #запись в лог файл
                    with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
                        log.write(user + ' - copied from server ' + data+'\n')
                    return file.read()
        except OSError as e:
            print(e)
            return 'Error'
    elif req.startswith('GET /disconnect/'): #обработка запроса 
        with open('/home/popov/PycharmProjects/FTP/log.txt', 'a+') as log:
            log.write(user + ' - disconnect\n')
        return 'Close connection'
    else:
        return 'Bad request'


def rmdir(path): #код команды rmdir
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


#развертывание сервера
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s...' % SERVER_PORT)
user = None
users = {'Admin':'qwerty', 'UserOne':'12345'}

while True: #запуск сервера
    content = ''
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
