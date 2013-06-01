#!/usr/bin/python2
# -*- coding: utf-8 -*-

import random, os
import logging
from lesson import Lesson

class Quiz():
    """
    A Quiz is composed of a set of lessons, a length and a mode (random, 
    ordered - currently only random is implemented).
    
    It is a blank copy of an exam.
    
    The exam object represents a set of answer to the quiz.
    """
    def __init__(self, name, length=10, mode='random'):
        self.name = name
        self.lessons = set()
        self.lessonsNames = set() # set of lessons' names, for fast searching
        self.mode = mode
        self.length = length
        self.words = []
        self.full_words = [] #complete list of all words from all lessons (used for infinite quiz)
        self.iter_index = -1
        self.techLogger = logging.getLogger('techLog')

    
    def add_lesson(self, name, path=os.getcwdu()):
        if isinstance(name, Lesson):
            self.techLogger.debug("adding lesson object: %s, path: %s" % (name.name, name.path))
            self.lessons.add(name)
            self.lessonsNames.add(name.name)
        else:
            #we consider name is the name of the lesson, and thus the directory.
            self.techLogger.debug("creating a lesson before adding it: %s, path: %s" % (name, path))
            lesson = Lesson(name, path)
            self.add_lesson(lesson)
    def remove_lesson(self, lesson):
	self.techLogger.debug("Trying to remove lesson %s" % lesson.name)
        if (lesson in self.lessons):
            self.lessonsNames.discard(lesson.name)
            self.lessons.remove(lesson)
	    self.techLogger.debug("Lesson '%s' removed!" % lesson.name)
            
    def __iter__(self):
        """
        Iterate through the list of words.
        """
        self.iter_index = -1
        return self
        
    def next(self):
        self.iter_index = self.iter_index + 1
        if self.iter_index >= len(self.words):
	    self.techLogger.debug("End of the list of word reached!")
            raise StopIteration
        word =  self.words[self.iter_index]
        self.techLogger("Next word chosen is: %s" % word)
        return word

    def get_next_word(self):
        index = 0
        while index < len(self.words):
            yield self.words[index]
            index += 1
    
    def generate(self):
        """
        Generate a list of words, based on the lessons (self.lessons), the desired 
        length (self.length), and the mode (self.mode, currently random only)
        """
        self.full_words = []
        for lesson in self.lessons:
            self.full_words += lesson.words
        self.techLogger.debug("Full list of words: %s" % ", ".join([s.word for s in self.full_words]))
        self.words = []
        # Avoid infinite loop if too much words are requested.
        if self.length > len(self.full_words):
            self.length = len(self.full_words) 
        local_full_words = self.full_words[:]
        while (len(self.words) < self.length):
            new_word = random.choice(local_full_words)
            self.words.append(new_word)
            local_full_words.remove(new_word)
	self.techLogger.debug("List of words in the quiz (length: %d): %s" % (len(self.words), ", ".join([w.word for w in self.words])))
        return self.words
    
    def get_random_word(self):
        word  = random.choice(self.full_words)
        self.techLogger.debug("New word chosen: %s" % word.word)
        return word
    
    def __unicode__(self):
        return "\n".join([unicode(w) for w in self.words])
        
    def pretty_print(self):
        s  = self.name + "\n" + "-" * len(self.name) + "\n"
        s += "%15s | %s\n" % ('word', 'file')
        s += '-' * 15 + ' | ' + '-' * 80 + '\n'
        for w in self.words:
            s += '%15s | %s\n' % (w.word, w.file)
        return s
        

if __name__ == "__main__":
    quiz = Quiz('test', 5)
    lesson = Lesson('mots1', os.path.normpath(os.getcwdu()+'/../resources/lessons/mots1'))
    quiz.add_lesson(lesson)
    quiz.generate()
    print quiz.pretty_print()
    quiz.length = 20
    quiz.generate()
    print quiz.pretty_print()
    
    word = quiz.next()
    while word is not None:
        print (unicode(word))
        word = quiz.next()
