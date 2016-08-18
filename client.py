# -*- coding: cp949 -*-

from socket import *
from select import select
import threading
import sys
import wx, gui

HOST = '115.68.27.153'
PORT = 50010
BUFSIZE = 1024
ADDR = (HOST, PORT)

# ���� ����
clientSocket = socket(AF_INET, SOCK_STREAM)

# ���� ���� �õ�
try:
	clientSocket.connect(ADDR)
except Exception:
	print("���� ���� ����")
	sys.exit()
print("���� ���� ����")

isConnect = True

def dataSend():
        global isConnect
        
        while isConnect:
                pass

def dataRecv():
        global isConnect
        
        while isConnect:
                read_socket, write_socket, error_socket = select([clientSocket], [], [], 0.1)
                
                if read_socket == [clientSocket]:
                        data = clientSocket.recv(BUFSIZE)
                        
                        if not data:
                                print("���� (%s : %s) ���� ����" % ADDR)
                                isConnection = False
                                return
                        
                        else:
                                print(data)

th1 = threading.Thread(target = dataSend, args = ())
th2 = threading.Thread(target = dataRecv, args = ())

th1.start()
th2.start()

app = wx.App(redirect = True)
top = gui.Frame("Client")
top.Show()
app.MainLoop()

isConnect = False

th1.join()
th2.join()

clientSocket.close()
sys.exit()
