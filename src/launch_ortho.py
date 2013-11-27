#!/usr/bin/python2
# -*- coding: iso-8859-15 -*-

# Sous Linux (Ubuntu), les paquets suivants sont nécessaires:
#  - python-wxgtk2.8
#  - python-pygame

import wx
import ortho.gui
from ortho.gui.gui_glue import GuiGlue
import logging

class OrthoApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        self.gg = GuiGlue() #singleton
        self.gg.initConfig()
        myMainFrame = ortho.gui.MainFrame(None, -1, "")
        self.SetTopWindow(myMainFrame)
        myMainFrame.Show()
        return 1
    
if __name__ == "__main__":
    myApp = OrthoApp(0)
    myApp.MainLoop()

