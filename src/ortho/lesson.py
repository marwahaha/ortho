#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from word import Word

class Lesson():
    """
    One Lesson is a set of words with a name.

    @param name: name of the lesson
    @type name: unicode

    @param path: full path of the folder containing the lesson's words
    @type path: unicode path (e.g. as returned from os.getcwdu())
    """
    def __init__(self, name, path=None):
        self.name = name
        self.words = [] #list of Word objects
        self.path = path
        if path is not None:
            self.load()

    
    def load(self):
        """
        Read the lesson's path, loading and creating words
        """
        if self.path is None:
            return False
        for file in os.listdir(self.path):
            full_file_name = os.path.join(self.path, file)
            if (os.path.isfile(full_file_name) and 
                os.path.splitext(file)[1] == ".wav"):
                word_name = os.path.splitext(file)[0]
                self.words.append(Word(word_name,full_file_name))
        return True
    
    def __unicode__(self):
        return u"<Name: %s; Words: %s>" % (self.name, ",".join([unicode(w) for w in self.words]))
    
if __name__ == "__main__":
    lesson = Lesson('mots1', os.path.normpath(os.getcwdu()+'/../mots1'))
    # lesson.load()
    print  unicode(lesson)
    