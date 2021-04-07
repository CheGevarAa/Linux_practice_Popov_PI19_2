import socket
import threading
import sys

global socks_list

def progress_bar(step, n):
    len = 60
    len_filled = int(round(len * step/n))
    len_unfilled = len - len_filled
    bar = "|"*len_filled+"-"*len_unfilled
    percent = round(100.0 * step/n, 1)
    if step == n - 1:
        dop = '\n'
    else:
        dop = '\r'
    sys.stdout.write(f'[{bar}] {percent}% {dop}')
    sys.stdout.flush()



class MyThread(threading.Thread):
    def __init__(self, host, n):
        super(self, name="thread" + str(n))
        self.host = host
        self.port = n

    def run(self):
        sock = socket.socket()
        try:
            sock.connect((self.host, self.port))
            with lock:
                socks_list.append(self.port)
        except:
            pass
        sock.close()

lock = threading.Lock()
n = 2**16 - 1

host = input('Type in the host:')
socks_list = []
threads = [MyThread(host, port) for port in range(1, n)]
for port in range(1, n):
    threads[port - 1].start()
    progress_bar(port, n)
[threads[port - 1].join() for port in range(1, n)]
socks_list.sort()
for port in socks_list:
    print("Port#", port, " is opened")