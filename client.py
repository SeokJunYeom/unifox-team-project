# -*- coding: utf-8 -*-

from socket import *
from select import select
import sys

HOST = '127.0.0.1'
PORT = 56789
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
