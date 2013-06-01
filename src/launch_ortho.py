#!/usr/bin/python2
# -*- coding: iso-8859-15 -*-

# Sous Linux (Ubuntu), les paquets suivants sont nécessaires:
#  - python-wxgtk2.8
#  - python-pygame

import wx
import ortho.gui
import logging

class OrthoApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        self._initLog()
        myMainFrame = ortho.gui.MainFrame(None, -1, "")
        self.SetTopWindow(myMainFrame)
        myMainFrame.Show()
        return 1
       
    def _initLog(self):
        self.techLogger = logging.getLogger('techLog')
        self.techLogger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('OrthoApp_debug.log', encoding="iso-8859-15")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s() - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        self.techLogger.addHandler(fh)
    
if __name__ == "__main__":
    myApp = OrthoApp(0)
    myApp.MainLoop()

