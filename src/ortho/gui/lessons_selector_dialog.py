#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from ortho.gui.gui_glue import GuiGlue

class LessonsSelectorDialog(wx.Dialog):
    """
    Modal dialog to choose the lessons.
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        
        self.gg = GuiGlue() #singleton
        
        # Lessons selector
        self.availableLessons = sorted(self.gg.searchLessons(),key=lambda lesson: lesson[0])
        self.lessonsCheckBoxes = [(wx.CheckBox(self, -1, lesson[0]), lesson[0], lesson[1])  
           for lesson in self.availableLessons]
        
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.onSelectAll, self.selectAll_btn)
        self.Bind(wx.EVT_BUTTON, self.onInvertSelect, self.invertSelect_btn)
        self.Bind(wx.EVT_RADIOBOX, self.onModeSelect, self.rmode)


    def __do_layout(self):
        self.SetTitle(u"Quelles leçons?")
        
        #top Sizer
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox2 = wx.BoxSizer(wx.HORIZONTAL) #for main buttons
        
        sbox1 = wx.StaticBox(self, -1, u"Leçons")
        vbox2 = wx.StaticBoxSizer(sbox1, wx.VERTICAL) #lessons selector
        vbox3 = wx.BoxSizer(wx.HORIZONTAL) #for selection button
        vbox4 = wx.BoxSizer(wx.VERTICAL) #for mode
        
        #create all lessons check boxes
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox6 = wx.BoxSizer(wx.VERTICAL)
        #gbox1_1_1_1 = wx.GridSizer(1+len(self.lessonsCheckBoxes) /2, 2, 2, 2)
        idx = 0
        for l in self.lessonsCheckBoxes:
            if self.gg.quiz is not None and l[1] in self.gg.quiz.lessonsNames:
                l[0].SetValue(True)
            #gbox1_1_1_1.Add(l[0], 0, wx.ALL | wx.ALIGN_LEFT, 2)
            if idx < len(self.lessonsCheckBoxes)/2+1:
                vbox5.Add(l[0], 0, wx.ALL | wx.ALIGN_LEFT, 2)
            else:
                vbox6.Add(l[0], 0, wx.ALL | wx.ALIGN_LEFT, 2)
            idx += 1
        #vbox2.Add(gbox1_1_1_1, 1, wx.ALL | wx.EXPAND, 2)
        hbox3.Add(vbox5, 1, wx.ALL | wx.EXPAND, 2)
        hbox3.Add(vbox6, 1, wx.ALL | wx.EXPAND, 2)
        vbox2.Add(hbox3, 1, wx.ALL | wx.EXPAND, 2)
        
        self.selectAll_btn = wx.Button(self, -1, "Tout choisir")
        self.invertSelect_btn = wx.Button(self, -1, u"Inverser la sélection")
        vbox3.Add(self.selectAll_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        vbox3.Add((20, 20), 0, wx.ALIGN_RIGHT, 0)
        vbox3.Add(self.invertSelect_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        vbox3.Add((20, 20), 0, wx.ALIGN_RIGHT, 0)
        vbox2.Add(vbox3, 0, wx.ALL | wx.EXPAND, 2)
        
        # Main buttons
        self.OK_1 = wx.Button(self, wx.ID_OK, "OK")
        self.cancel_1 = wx.Button(self, wx.ID_CANCEL, "Annuler")
        hbox2.Add((20, 20), 0, wx.ALIGN_RIGHT, 0)
        hbox2.Add(self.OK_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        hbox2.Add((20, 20), 0, wx.ALIGN_RIGHT, 0)
        hbox2.Add(self.cancel_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        hbox2.Add((20, 20), 0, wx.ALIGN_RIGHT, 0)
        
         # Mode
        self.rmode = wx.RadioBox(self, -1, "Quel mode?", 
            choices=["Interrogation", "En continu"], majorDimension=1, 
            style=wx.RA_SPECIFY_COLS)
        self.rmode.SetSelection(self.gg.mode)
        self.length_lbl = wx.StaticText(self, -1, u"Nombre de questions")
        self.length_txt = wx.TextCtrl(self, -1, str(self.gg.length))
        self.length_txt.SetMaxLength(3)
        if self.gg.mode == 1:
            self.length_txt.Enable(False)
        vbox4.Add(self.rmode, 0, 0, 0)
        vbox4.Add(self.length_lbl, 0, 0, 0)
        vbox4.Add(self.length_txt, 0, 0, 0)
        
        hbox1.Add(vbox2, 0, 0, 0)
        hbox1.Add((5,5), 0, 0, 0)
        hbox1.Add(vbox4, 0, 0, 0)
        
        
        vbox1.Add(hbox1, 1, wx.ALL | wx.ALIGN_RIGHT, 2)
        vbox1.Add(hbox2, 0, wx.ALL | wx.ALIGN_RIGHT, 2)
        self.SetSizer(vbox1)
        vbox1.Fit(self)
        self.Layout()
        self.Centre()
        
    def onModeSelect(self, event):
        """
        Called when a mode radio button is clicked.
        The goal is to enable/disable question length depending on the mode.
        """
        idx = self.rmode.GetSelection()
        if idx == 0: #interrogation mode
            self.length_txt.Enable(True)
        elif idx == 1: #never ending exercise
            self.length_txt.Enable(False)
    
    def onSelectAll(self, event):
        for l in self.lessonsCheckBoxes:
            l[0].SetValue(True)
    
    def onInvertSelect(self, event):
        for l in self.lessonsCheckBoxes:
            l[0].SetValue(not l[0].GetValue())

    def onOK(self, event):
        """
        Create a quiz object with the selected lessons.
        """
        self.gg.length = int(self.length_txt.GetValue().strip())
        self.gg.mode = self.rmode.GetSelection()
        self.gg.createQuiz(self.lessonsCheckBoxes)
        # self.GetParent().quiz = Quiz(name="test", length=10)
        # for lesson in self.lessonsCheckBoxes:
            # if (lesson[0].IsChecked()):
                # self.GetParent().quiz.add_lesson(name=lesson[1], path=lesson[2])
        # self.GetParent().quiz.generate()
        # if (self.rmode.GetSelection() == 1):
            # self.GetParent().orthoApp.usePredefinedOrder()
        self.EndModal(wx.ID_OK)

    def onCancel(self, event): 
        self.EndModal(wx.ID_CANCEL)
