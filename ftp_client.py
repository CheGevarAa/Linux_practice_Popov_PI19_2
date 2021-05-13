import socket #импорт библиотеки для работы
HOST = 'localhost' #адрес хоста
PORT = 8000 #подключаемый порт

requests = ['GET /connect/UserOne/12345', 'GET /pwd/', 'GET /mkdir/myfolder', 'GET /ls/', 'GET /rename/myfolder//documents',
            'GET /rmdir/myfolder', 'GET /rmfile/', 'GET /toclient/documents/text.txt', 'GET /disconnect/'] #список запросов для обработки
#циклом проверяем работу по всем запросам сразу
for request in requests:
    sock = socket.socket() #подключение к сокету
    try:
        sock.connect((HOST, PORT)) #в начаое проверка возможности подключения к хосту и порту
    except Exception as e: 
        print(e) #если невозможно, вывод ошибки
    print(request) #вывод запроса который был отправлен
    sock.send(request.encode()) #перевод текстового запроса в поток байт
    response = sock.recv(8192).decode() #обратный процесс для получения ответа
    if response == 'error':#проверка наличия ошибки и ее вывод, если она обнаружена, если нет, вывод ответа 
        print('Error in ' + request)
    else:
        print(response)

    sock.close()#закрытие подключения
