#!/usr/bin/python

# A frame is the main window of the application. It contains the mainPanel
# (another class) and defines the menu bar.

import wx
import ortho.gui

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyGladedFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.myMenuBar = wx.MenuBar()
        self.menu_item = wx.Menu()
        self.load_item = wx.MenuItem(self.menu_item, wx.NewId(), "&Charger une liste de mots...", "", wx.ITEM_NORMAL)
        self.menu_item.AppendItem(self.load_item)
        self.quit_item = wx.MenuItem(self.menu_item, wx.ID_EXIT, "&Quitter", "Quitter l'application", wx.ITEM_NORMAL)
        self.menu_item.AppendItem(self.quit_item)
        self.myMenuBar.Append(self.menu_item, "&Menu")
        self.SetMenuBar(self.myMenuBar)
        # Menu Bar end
        self.mainPanel = ortho.gui.MainPanel(self, -1)
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.onMenuSelectLessons, self.load_item)
        self.Bind(wx.EVT_MENU, self.onQuit, self.quit_item)
        self.Bind(wx.EVT_CLOSE, self.onQuit)

    def __set_properties(self):
        self.SetTitle("Mes mots d'orthographe")
        self.SetSize((797, 298))
        self.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.mainPanel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        self.Layout()
        self.Centre()

    def onQuit(self, event):
        self.OnCloseWindow()
        
    def OnCloseWindow(self):
        dial  = wx.MessageDialog(None, 'Veux-tu vraiment quitter?', 'Question', 
                wx.YES_NO | wx.NO_DEFAULT |wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            # self.orthoApp.logScore()
            # score = wx.MessageDialog(None, self.orthoApp.getScore(), 'Ton score', wx.OK |wx.ICON_INFORMATION)
            # score.ShowModal()
            self.Destroy()
    
    def onMenuSelectLessons(self, event):
        """
        Called when clicking on the menu option "Charger une liste de mots...".
        """
        dial = ortho.gui.LessonsSelectorDialog(self)
        return dial.ShowModal()
