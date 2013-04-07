#!/usr/bin/python2
# -*- coding: utf-8 -*-
import platform
#platform.system() is either Windows or Linux

if platform.system() == 'Windows':
    osName = 'Windows'
    import winsound
else:
    osName = 'Linux'
    try:
        import pygame
        pygame.init()
    except ImportError:
        print "Impossible de charger le module pygame.  Il faut installer le paquet python-pygame"
        raise

class Word():
    def __init__(self, word, file_name):
        self.word = word
        self.file = file_name
        # print "New word created: %s" % self.word
       
    def is_answer_correct(self, answer):
        if (answer.strip() == self.word):
            return True
        else:
            return False

    def __unicode__(self):
        return u"(%s, %s)" % (self.word, self.file)
    
    
    def play(self):
        if osName == 'Windows':
            winsound.PlaySound(self.file.encode('latin1'), winsound.SND_FILENAME)
        else:
            if pygame.mixer.music.get_busy():
                #pygame.mixer.music.queue(self.file.encode('latin1'))
                pygame.mixer.music.queue(self.file.encode('UTF-8'))
            else:
                #pygame.mixer.music.load(self.file.encode('latin1'))
                pygame.mixer.music.load(self.file.encode('UTF-8'))
                pygame.mixer.music.play()
    
