import wx
from DBController import DBConnection
from GUI import MainFrame


app   = wx.App()
frame = MainFrame(None)
frame.Show(True)
app.MainLoop()
