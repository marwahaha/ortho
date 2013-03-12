#!/usr/bin/python
# -*- coding: utf-8 -*-

import os #for path.*
from ortho import Quiz
from ortho import Exam

class GuiGlue:
    # see http://stackoverflow.com/a/6255101 for "singleton" pattern
    __shared_dict = {}
    def __init__(self):
        self.__dict__ = self.__shared_dict
        if not hasattr(self, 'quiz'):
            self.quiz = None
        if not hasattr(self, 'exam'):
            self.exam = None
        if not hasattr(self, 'length'):
            self.length = 10
        if not hasattr(self, 'mode'):
            self.mode = 1 #Training mode by default
        self.lessonsPath = os.path.normpath(os.getcwdu() +  "/resources/lessons/")
    
    def searchLessons(self, basePath=None):
        """
        Assumption: all folders in basePath are a lesson.
        
        @param basePath: base folder where to search for lessons
        @type basePath: unicode - absolute path name
        
        @return: an array of tuples (lesson's name, lesson's absolute path)
        @rtype: array of tuples
        """
        if basePath:
            self.lessonsPath = basePath
        lessons = [(f, os.path.join(self.lessonsPath, f)) for f in os.listdir(self.lessonsPath)
            if os.path.isdir(os.path.join(self.lessonsPath, f))]
        return lessons
     
    def createQuiz(self, lessonsCheckBoxes):
        """
        Create a quiz based on the checked check boxes.
        """
        self.quiz = Quiz(name="test", length=self.length)
        for lesson in lessonsCheckBoxes:
            if (lesson[0].IsChecked()):
                print "Lesson to add: %s - %s" % (lesson[1], lesson[2])
                self.quiz.add_lesson(name=lesson[1], path=lesson[2])
        self.quiz.generate()
        self.quiz.pretty_print()
    
    def startExam(self):
        self.exam = Exam("Eléa", self.quiz)
    
    def endExam(self):
        self.exam.correct()
        return u"Ton score est de %d sur %d" % (self.exam.score, self.quiz.length)
    
    def getNextWord(self, answer=None):
        if answer is not None:
            self.exam.answers.append(answer)
        if self.mode == 0:
            return self.quiz.next()
        else:
            return self.quiz.get_random_word()
    
    def getExamStatus(self):
        """
        Return a string giving the status of the exam: how many answer given.
        """
        return u"%d mots répondus sur %d au total" % (len(self.exam.answers), self.quiz.length)
    def getExamDetails(self):
        """
        Return a multiline string with the mistakes
        """
        if self.exam.score != self.quiz.length:
            res = u"Tu t'es trompé sur les mots suivants:"
            for index in self.exam.mistakes:
                answer = self.exam.answers[index]
                word = self.quiz.words[index].word
                res += "\n" + u"%25s --> %s" % (word, answer)
        else:
            res =  "Magnifique %s!" % self.exam.student
        
        return res
    