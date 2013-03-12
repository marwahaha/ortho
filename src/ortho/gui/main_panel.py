#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from ortho.gui.gui_glue import GuiGlue
from lessons_selector_dialog import LessonsSelectorDialog
from ortho import Word #for playing "bravo" sound

class MainPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyGladedPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.title_lbl = wx.StaticText(self, -1, u"Exercice d'orthographe pour Eléa", style=wx.ALIGN_CENTRE)
        self.reponse_lbl = wx.StaticText(self, -1, u"Réponse: ", style=wx.ALIGN_RIGHT)
        self.responseCtrl = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER | wx.TE_RICH)
        self.resultat_lbl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.start_btn = wx.Button(self, -1, u"Démarrer!")
        self.repeat_btn = wx.Button(self, -1, u"Répéter")
        self.next_btn = wx.Button(self, -1, "Suivant")
        self.score_lbl = wx.StaticText(self, -1, "Score")
        self.end_btn = wx.Button(self, -1, "Terminer l'exercice")
        self.mode = 0 #default mode: Exam
        self.correct = 0 #for training
        self.wrong = 0 #for training too
        self.__set_properties()
        self.__do_layout()
        
        
        self.Bind(wx.EVT_TEXT_ENTER, self.onNextClickExam, self.responseCtrl)
        self.Bind(wx.EVT_BUTTON, self.onStartClick, self.start_btn)
        self.Bind(wx.EVT_BUTTON, self.onRepeatClick, self.repeat_btn)
        self.Bind(wx.EVT_BUTTON, self.onNextClickExam, self.next_btn)
        self.Bind(wx.EVT_BUTTON, self.onQuit, self.end_btn)
        # end wxGlade
        
        self.timer = wx.Timer(self, -1)
        self.redStyle = wx.TextAttr(wx.RED)
        self.greenStyle = wx.TextAttr(wx.Colour(0,255,0))
        self.bravoSound = Word("bravo", "resources/bravo.wav")
        self.errorSound = Word("error", "resources/error.wav")
        self.gg = GuiGlue() #singleton
        
    def __set_properties(self):
        self.title_lbl.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.responseCtrl.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.responseCtrl.Enable(False)
        self.resultat_lbl.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.repeat_btn.Enable(False)
        self.next_btn.Enable(False)
        self.score_lbl.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

    def __do_layout(self):
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.title_lbl, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 8)
        sizer_7.Add((5, 5), 0, wx.ALIGN_RIGHT, 0)
        sizer_7.Add(self.reponse_lbl, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add((5, 5), 0, 0, 0)
        sizer_7.Add(self.responseCtrl, 6, wx.EXPAND, 0)
        sizer_7.Add((5, 5), 0, 0, 0)
        sizer_5.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_6.Add((5, 5), 0, 0, 0)
        sizer_6.Add(self.resultat_lbl, 6, wx.EXPAND, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.Add(self.repeat_btn, 0, 0, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.Add(self.next_btn, 0, 0, 0)
        sizer_6.Add((5, 5), 0, 0, 0)
        sizer_5.Add(sizer_6, 1, wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_RIGHT, 5)
        sizer_3.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_4.Add((5, 5), 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(self.score_lbl, 1, 0, 0)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.start_btn, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.end_btn, 0, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        sizer_4.Add((5, 5), 0, 0, 0)
        sizer_3.Add(sizer_4, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 5)
        self.SetSizer(sizer_3)
        sizer_3.Fit(self)

    def _endExam(self):
        self.score_lbl.SetLabel(self.gg.endExam())
        self.resultat_lbl.SetValue(self.gg.getExamDetails())
    
    def _refreshConfig(self):
        """
        Called when a configuration has been changed via the menu.
        """
        if self.gg.mode == self.mode:
            return
        
        # change of mode: unbind nextClick
        self.mode = self.gg.mode
        if self.mode == 0:
            #Exam mode
            self.Unbind(wx.EVT_BUTTON, source=self.next_btn)
            self.Unbind(wx.EVT_TEXT_ENTER, source=self.responseCtrl)
            
            self.Bind(wx.EVT_BUTTON, self.onNextClickExam, self.next_btn)
            self.Bind(wx.EVT_TEXT_ENTER, self.onNextClickExam, self.responseCtrl)
        else:
            # Training mode
            self.Unbind(wx.EVT_BUTTON, source=self.next_btn)
            self.Unbind(wx.EVT_TEXT_ENTER, source=self.responseCtrl)
            
            self.Bind(wx.EVT_BUTTON, self.onNextClickTraining, self.next_btn)
            self.Bind(wx.EVT_TEXT_ENTER, self.onNextClickTraining, self.responseCtrl)
            
            
    
    def onQuit(self, event):
        # print "Event at MyGladedPanel Level"
        if self.mode == 0:
            self._endExam()
        self.GetParent().OnCloseWindow()
    def onRepeatClick(self, event):
        # print "Event handler `onRepeatClick' implemented"
        self.word.play()

    def onNextClickExam(self, event):
        try:
            self.chooseNewWord(self.responseCtrl.GetValue().strip())
        except StopIteration:
            self._endExam()
    
    def onNextClickTraining(self, event):
        if self.responseCtrl.GetValue().strip() == self.word.word:
            self.responseCtrl.SetStyle(0, self.responseCtrl.GetLastPosition(), self.greenStyle)
            self.resultat_lbl.AppendText(u'\nBravo! Le mot était: %s' % self.word.word)
            ## to force refresh of the window, otherwise 
            ## the resultat_lbl is not updated before the sound.
            # self.Update() 
            self.correct += 1
            self.bravoSound.play()
            self.chooseNewWord()
        else:
            # print "c'est faux!"
            self.wrong += 1
            self.resultat_lbl.AppendText(u"\nCe n'est pas juste... Tu as écrit: %s" % self.responseCtrl.GetValue().strip())
            self.errorSound.play()
            self.resultat_lbl.Show(True)
            self.responseCtrl.SetFocus()
            self.responseCtrl.SetStyle(0, self.responseCtrl.GetLastPosition(), self.redStyle)


    
    def onStartClick(self, event):
        print "Event handler `onStartClick' started!"  
        
        if not self.gg.quiz:
            dial = LessonsSelectorDialog(self)
            dial.ShowModal()
        if not self.gg.quiz:
            return
        else:
            self._refreshConfig()
            
        self.responseCtrl.Enable(True)
        self.gg.startExam()
        self.chooseNewWord()
        
        self.start_btn.Hide()
        self.repeat_btn.Enable(True)
        self.next_btn.Enable(True)
        

    def chooseNewWord(self, answer=None):
        self.responseCtrl.Clear()
        self.word = self.gg.getNextWord(answer)
        if self.mode == 0:
            self.score_lbl.SetLabel(self.gg.getExamStatus())
        self.word.play()
        self.responseCtrl.SetFocus()