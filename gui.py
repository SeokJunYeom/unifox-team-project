# -*- coding: utf-8 -*-

import wx

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title = title, size = (350, 200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnClose(self, event):
        dlg = wx.MessageDialog(self, "Confirm Exit", "Close?", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        
        if result == wx.ID_OK:
            self.Destroy()
            
if __name__ == "__main__":
    app = wx.App(redirect = True)
    top = Frame("Hello World")
    top.Show()
    app.MainLoop()
