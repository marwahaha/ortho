#!/usr/bin/python2
# -*- coding: iso-8859-15 -*-

# Sous Linux (Ubuntu), les paquets suivants sont nécessaires:
#  - python-wxgtk2.8
#  - python-pygame

import wx
import ortho.gui

class OrthoApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        myMainFrame = ortho.gui.MainFrame(None, -1, "")
        self.SetTopWindow(myMainFrame)
        myMainFrame.Show()
        return 1
       
if __name__ == "__main__":
    myApp = OrthoApp(0)
    myApp.MainLoop()

    
#TODO
# - logging for parents
# - when changing the lessons or the mode, "reset" the interface and the state of the application
# - at the end of an interrogation, list the correct words in the textpanel
# - When closing the application, display a specific window with score & faults
# - TECHOS: enhance the way the lessons are managed in GuiGlue
# - TECHOS: why on Linux, the menu bar is not showing up at the start of the application?
#
#DONE
# - check box "un/select all lessons"
# - order lessons check boxes by name
# - score dialog box
# - status bar update after each word
# - Interrogation mode
# - training mode
