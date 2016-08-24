# -*- coding: cp949 -*-

from socket import *
from select import select
import imgProcess
import threading
import sys

HOST = '104.214.146.144'
PORT = 50010
BUFSIZE = 1024
ADDR = (HOST, PORT)

class Client():
        isConnect = True
        
        def __init__(self):
                # 소켓 생성
                self.clientSocket = socket(AF_INET, SOCK_STREAM)


                # 서버 연결 시도
                try:
                        self.clientSocket.connect(ADDR)
                        
                except Exception:
                        self.isConnect = False

        def imgSend(self, img, imgName):
                self.clientSocket.send(imgProcess.imgToString(img, imgName))

        def dataSend(self, str):
                self.clientSocket.send(str)

        def dataRecv(self):
                data = self.clientSocket.recv(BUFSIZE)

                if data.split("*")[0] == "image":
                        imgName = data.split("*")[1]
                        imgLen = data.split("*")[2]
                        imgData = data[int(len(imgLen)) + int(len(imgName)) + 8:]

                        imgData = self.revall(imgData, self.clientSocket, int(imgLen) - len(imgData))

                        return imgData

                else:
                        return data

        def revall(self, buf, sock, count):
                while count:
                        newbuf = sock.recv(count)

                        if not newbuf:
                                return None

                        buf += newbuf
                        count -= len(newbuf)

                return buf

        def __del__(self):
                if self.isConnect:
                        self.isConnect = False
                        self.clientSocket.close()

