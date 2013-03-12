#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
from quiz import Quiz

class Exam():
    def __init__(self, student, quiz):
        self.student = student
        self.quiz = quiz
        self.answers = []
        self.score = 0
        self.mistakes = []
    
    def correct(self):
        """
        Verify the answers against the quiz, calculate the score, and store
        in self.mistakes the list of bad words.
        """
        self.score = 0
        for index in range(len(self.answers)):
            if self.answers[index] == self.quiz.words[index].word:
                self.score = self.score + 1
            else:
                self.mistakes.append(index)

class ExamRunner():
    def __init__(self, student, quiz):
        self.exam = Exam(student, quiz)
        self.quiz = quiz
        
    def do_exam(self):
        """
        Actually run the exam. Ask questions and collect answers.
        """
        for word in quiz:
            #print word.word
            #winsound.PlaySound(word.file.encode('latin1'), winsound.SND_FILENAME)
            word.play()
            answer = raw_input(u"Ecris le mot que tu as entendu: ")
            answer = answer.strip().decode(sys.stdin.encoding)
            self.exam.answers.append(answer)
        print "Fin de l'examen."
    
    
    def get_score(self):
        """
        Correct the exam and print the score.
        """
        self.exam.correct()
        print u"Ton score est de %d sur %d" % (self.exam.score, self.quiz.length)
        if self.exam.score != self.quiz.length:
            print u"Tu t'es trompé sur les mots suivants:"
            for index in self.exam.mistakes:
                answer = self.exam.answers[index]
                word = self.quiz.words[index].word
                print "%25s --> %s" % (word, answer)
        else:
            print u"Magnifique %s!" % self.exam.student
            
            
if __name__ == "__main__":
    import os
    from lesson import Lesson
    quiz = Quiz("test", 15)
    lesson = Lesson('mots17', os.path.normpath(os.getcwdu()+'/../mots17'))
    quiz.add_lesson(lesson)
    quiz.generate()
    exam_runner = ExamRunner(u"Eléa", quiz)
    exam_runner.do_exam()
    exam_runner.get_score()
