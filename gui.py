# -*- coding: cp949 -*-

import wx
import os, sys
import imgProcess, imgEdit
import client

class MyFrame(wx.Frame):
    haveImg = False
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, "SeokJun Handsome", wx.DefaultPosition, wx.Size(1000,800))

        # �޴��� ����
        self.CreateStatusBar()
        menuBar = wx.MenuBar()

        # �޴� ����
        file = wx.Menu()
        server = wx.Menu()
        help = wx.Menu()
        edit = wx.Menu()
        
        # file �޴��� �߰�
        file.Append(101, "&Open", "Open a file")
        file.Append(102, "&Save", "Save a file")

        # server �޴��� �߰�
        server.Append(201, "&Send", "Send a file to server")
        server.Append(202, "&Receive", "Recive a file from server")

        # help �޴��� �߰�
        help.Append(301, "&Help", "How to use")
        help.AppendSeparator()
        help.Append(302, "&Developer", "People to develop")

        # edit �޴��� �߰�
        edit.Append(401, "&RGB", "Change RGB in image")
        edit.Append(402, "&EDGE", "Shows only edge")

        # �޴��ٿ� ������ �޴� �߰�
        menuBar.Append(file, "&File")
        menuBar.Append(server, "&Server")
        menuBar.Append(help, "&Help")
        menuBar.Append(edit, "&Edit")

        # �����ӿ� �޴��� ����
        self.SetMenuBar(menuBar)

        # �޴��� �̺�Ʈ �Լ� ����
        self.Bind(wx.EVT_MENU, self.openFile, id = 101)
        self.Bind(wx.EVT_MENU, self.saveFile, id = 102)

        self.Bind(wx.EVT_MENU, self.sendFile, id = 201)
        self.Bind(wx.EVT_MENU, self.recvFile, id = 202)

        self.Bind(wx.EVT_MENU, self.helpp, id = 301)
        self.Bind(wx.EVT_MENU, self.info, id = 302)

        self.Bind(wx.EVT_MENU, self.rgb, id = 401)
        self.Bind(wx.EVT_MENU, self.edge, id = 402)

#----------------------------------------------------------------------------------------------------------
# file �޴�
        
    wildcard = "pictures (*.jpeg,*.jpg)|*.jpeg;*.jpg"
    
    def openFile(self, event):
        dlg = wx.FileDialog(self, "Choose a image", os.getcwd(), "", self.wildcard , wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            # ������ ��ο� �̸��� ����
            self.imgPath = dlg.GetPath()
            self.imgName = os.path.basename(self.imgPath)

            self.img = imgProcess.imgRead(self.imgPath)
            self.haveImg = True

            # panel ���� �� �� ���� image ���
            panel = wx.Panel(self, -1, (0, 0), (1000, 800), style = wx.SUNKEN_BORDER)
            picture = wx.StaticBitmap(panel)
            picture.SetFocus()
            picture.SetBitmap(self.resize(wx.Bitmap(self.imgPath), 1000, 800))
            
        dlg.Destroy()

    def saveFile(self, event):
        dlg = wx.FileDialog(self, "Save a file", os.getcwd(), "", "*.jpg", wx.SAVE | wx.OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            imgPath = dlg.GetPath()
            imgName = os.path.basename(imgPath)

            imgProcess.imgSave(imgPath, self.img)

        dlg.Destroy()
            
    def resize(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)

        return result

#----------------------------------------------------------------------------------------------------------
# server �޴�

    def sendFile(self, event):
        cli = client.Client()

        if cli.isConnect:
            if self.haveImg:
                cli.imgSend(self.img, self.imgName)
                dlg = wx.MessageDialog(self, "A file is succesfuly sended.", "SUCCES", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()

            else:
                self.imgError()

        # ���� ������ �ȵ� ���� ó��
        else:
            dlg = wx.MessageDialog(self, "Client is not connecting Server.", "ERROR", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        del cli

    def recvFile(self, event):
        cli = client.Client()

        if cli.isConnect:
            cli.dataSend("request*dir")
            dir = cli.dataRecv()

            dlg = wx.TextEntryDialog(self, dir)
            dlg.SetValue("Input a file name.")

            if dlg.ShowModal() == wx.ID_OK:
                self.imgName = dlg.GetValue()
                
                cli.dataSend("request*" + self.imgName)
                self.imgStr = cli.dataRecv()
                self.img = imgProcess.imgDecode(self.imgStr)

                self.haveImg = True

                self.imgShow(self.img, "")
            

        else:
            dlg = wx.MessageDialog(self, "Client is not connecting Server.", "ERROR", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

        del cli
    
#----------------------------------------------------------------------------------------------------------
# help �޴�

    def helpp(self, event):
        dlg = wx.MessageDialog(self, "��-������ �� �� ��ģ �� ������ ��û�Ѵ�.", "Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def info(self, event):
        dlg = wx.MessageDialog(self, "<���� ���>\n������, �����, ����", "Info", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
#----------------------------------------------------------------------------------------------------------
# edit �޴�

    def rgb(self, event):
        if not self.haveImg:
            self.imgError()

        else:
            dlg = RGBdlg(None, -1, "RGB")
            dlg.ShowModal()
            dlg.Destroy()

            self.img = imgEdit.colorChange(self.img, dlg.getValue())
            self.imgShow(self.img, "rgb_")

    def edge(self, event):
        if not self.haveImg:
            self.imgError()

        else:
            self.img = imgEdit.edge(self.img)
            self.imgShow(self.img, "edge_")

    def imgShow(self, img, str):
        path = "image/" + str + self.imgName
        imgProcess.imgSave(path, img)
        
        panel = wx.Panel(self, -1, (0, 0), (1000, 800), style = wx.SUNKEN_BORDER)
        picture = wx.StaticBitmap(panel)
        picture.SetFocus()
        picture.SetBitmap(self.resize(wx.Bitmap(path), 1000, 800))

    def imgError(self):
        dlg = wx.MessageDialog(self, "You have to open a image file.", "Not image", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

#----------------------------------------------------------------------------------------------------------

class RGBdlg(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size = (200, 150))

        wx.StaticText(self, -1, 'Red', (15, 15))
        self.red = wx.SpinCtrl(self, -1, '1', (55, 10), (60, -1), min = -255, max = 255)
        
        wx.StaticText(self, -1, 'Green', (15, 40))
        self.green = wx.SpinCtrl(self, -1, '1', (55, 35), (60, -1), min = -255, max = 255)
        
        wx.StaticText(self, -1, 'Blue', (15, 65))
        self.blue = wx.SpinCtrl(self, -1, '1', (55, 60), (60, -1), min = -255, max = 255)
        
        cl = wx.Button(self, 1, 'Ok', (70, 90), (60, -1))

        cl.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, event):
        self.Close(True)

    def getValue(self):
        tu = (self.red.GetValue(), self.green.GetValue(), self.blue.GetValue())

        return tu
        
class MyApp(wx.App):
    def OnInit(self):
        myframe = MyFrame(None, -1, "")
        myframe.CenterOnScreen()
        myframe.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
