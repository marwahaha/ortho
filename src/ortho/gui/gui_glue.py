#!/usr/bin/python
# -*- coding: utf-8 -*-

import os #for path.*
import ConfigParser 
import logging, logging.handlers
from ortho import Quiz
from ortho import Exam

class GuiGlue:
    # see http://stackoverflow.com/a/6255101 for "singleton" pattern
    __shared_dict = {}
    
    __default_config = {
        'lessons_path'          : '/usr/share/ortho/lessons',
        'log_path'              : '/var/log/ortho',
        'technical_log_filename': 'ortho_tech.log',
        'technical_log_level'   : 'ERROR',
        'teacher_log_filename'  : 'ortho_teacher.log',
        'teacher_log_level'     : 'INFO',
        'dummy for test'        : 'toto'
    }
    
    def __init__(self):
        self.__dict__ = self.__shared_dict
        self.techLogger = logging.getLogger('techLog')
        if not hasattr(self, 'quiz'):
            self.quiz = None
        if not hasattr(self, 'exam'):
            self.exam = None
        if not hasattr(self, 'length'):
            self.length = 10
        if not hasattr(self, 'mode'):
            self.mode = 1 #Training mode by default
        if not hasattr(self, 'config'):
            self.config = ConfigParser.ConfigParser(self.__default_config)
            self.loadConfigFile()
        
    
    def loadConfigFile(self):
        """
        Load a configuration file.
        
        The locations are:
         - /etc/ortho
         - $HOME
         - $HOME/.config/ortho
         - folder pointed by environment variable $ORTHO_CONF
         - current directory
        The folder are read in that order, from the most general to the most specific.
        
        The filename must be: ortho.conf
        """
        for loc in '/etc/ortho', os.path.expanduser("~"), os.path.expanduser("~/.config/ortho"), os.environ.get("ORTHO_CONF",os.curdir), os.curdir:
            try: 
                 self.techLogger.debug('Trying to read config file: %s...' % os.path.join(loc, 'ortho.conf'))
                 with open(os.path.join(loc,"ortho.conf")) as source:
                    self.config.readfp( source )
                    self.techLogger.debug("Done.")
            except IOError:
                self.techLogger.debug("Failed: the file does not exist!")
                pass
        # Normalize paths and dump the configuration to the techLogger
        self.techLogger.debug(self.config.sections())
        sections = self.config.sections()
        sections.sort()
        for s in sections:
            for (key, val) in self.config.items(s):
                if key.endswith('path'):
                    val = os.path.expanduser(os.path.expandvars(val))
                    self.config.set(s,key,val)
                if key.endswith('log_level'):
                    val = val.upper()
                    self.config.set(s,key,val)

    def dumpConfiguration(self):
        sections = self.config.sections()
        sections.sort()
        config_str = "Loaded configuration:\n"
        for s in sections:
            config_str += s + '\n'
            keys = self.config.options(s)
            keys.sort()
            for key in keys:
                config_str += ' - %-25s : %s\n' % (key, self.config.get(s, key))
        return config_str
        
    
    def initConfig(self):
        """
        Based on the current configuration, set up necessary stuffs, like
        logging, folders...
        """
        self._initLog()
        self.techLogger.debug(self.dumpConfiguration())
        
    
    
    def _initLog(self):

        # create logging directory if it does not exist yet.
        for log_path in (self.config.get('default', 'technical_log_path'), self.config.get('default', 'teacher_log_path')):
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            elif not os.path.isdir(log_path):
                raise Exception("log dir is not a directory!")
        
        # create technical_log
        self.techLogger = logging.getLogger('techLog')
        self.techLogger.setLevel(self.config.get('default', 'technical_log_level'))
        fh = logging.handlers.RotatingFileHandler(os.path.join(
            self.config.get('default', 'technical_log_path'), 
            self.config.get('default', 'technical_log_filename')),
            mode='a', maxBytes=1024*1024, backupCount=5, encoding='utf-8')
        fh.setLevel(self.config.get('default', 'technical_log_level'))
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s() - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        self.techLogger.addHandler(fh)
        
         # create teacher_log
        self.teacherLogger = logging.getLogger('teacher')
        self.teacherLogger.setLevel(self.config.get('default', 'teacher_log_level'))
        teacher_log_filename = os.path.join(
            self.config.get('default', 'teacher_log_path'), 
            self.config.get('default', 'teacher_log_filename'))
        fh = logging.handlers.RotatingFileHandler(teacher_log_filename, mode='a', maxBytes=1024*1024, backupCount=5, encoding='utf-8')
        fh.setLevel(self.config.get('default', 'teacher_log_level'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        self.teacherLogger.addHandler(fh)
        self.techLogger.info("Teacher Logs opened. Filename is: %s" % teacher_log_filename)
    
    def searchLessons(self):
        """
        Assumption: all folders in basePath are a lesson.
        
        @param basePath: base folder where to search for lessons
        @type basePath: unicode - absolute path name
        
        @return: an array of tuples (lesson's name, lesson's absolute path)
        @rtype: array of tuples
        """
        lessonsPath = self.config.get('default', 'lessons_path')
        lessons = [(f, os.path.join(lessonsPath, f)) for f in os.listdir(lessonsPath)
            if os.path.isdir(os.path.join(lessonsPath, f))]
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
    
