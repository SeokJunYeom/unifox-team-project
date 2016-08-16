# -*- coding: utf-8 -*-

from socket import *
from select import select
from multiprocessing import Process, Queue
import sys

HOST = '115.68.27.153'
PORT = 50010
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 생성
clientSocket = socket(AF_INET, SOCK_STREAM)

# 서버 연결 시도
try:
	clientSocket.connect(ADDR)
except Exception:
	print("서버 연결 실패")
	sys.exit()
print("서버 연결 성공")

def dataSend():
        message = sys.stdin.readline()
        clientSocket.send(message.encode())

def dataRecv(queue):
        while True:
                read_socket, write_socket, error_socket = select([clientSocket], [], [], 10)

                if read_socket == [clientSocket]:
                        data = clientSocket.recv(BUFSIZE)

if __name__ == "__main__":
        queue = Queue()
        p = Process(target = dataRecv, args = (queue,))
        p.start()

        while True:
                try:
                        dataSend()

                        if queue.qsize() > 0:
                                data = queue.get()
                                print(data)
                                
                                if not data:
                                        print("서버 (%s : %s) 와의 연결 끊김." % ADDR)
                                        p.join()
                                        clientSocket.close()
                                        sys.exit()

                                else:
                                        pass

                except KeyboardInterrupt:
                        p.join()
                        clientSocket.close()
                        sys.exit()
