#!/usr/bin/python
# give root lesson path as first argument of the script
# ex: $ create_words_list.sh ./resources/lessons
import os,sys

lessons_path = os.path.join(os.getcwd(), sys.argv[1])   
words_list_name = "words.list"

print "Lesson path: %s" % lessons_path

def create_words_list(full_dir, file_name=words_list_name):
    print "    Creating %s for lesson %s..." % (file_name, os.path.basename(full_dir))
    fw = open(os.path.join(full_dir, file_name), 'w')
    for f in os.listdir(full_dir):
        print "      Analysing file %s..." % f
        if (os.path.isfile(os.path.join(full_dir,f)) and os.path.splitext(f)[1] == ".wav"):
            print "      File %s added." % f
            fw.write("%s;%s\n" % (f, os.path.splitext(f)[0]))
    fw.close()
    
    
for dir in os.listdir(lessons_path):
    full_dir = os.path.join(lessons_path, dir)
    if os.path.isdir(full_dir):
        print "  Lesson %s found..." % dir
        if os.path.isfile(os.path.join(full_dir, words_list_name)):
            print "    words.list exists, I will not overwrite it."
        else:
            create_words_list(full_dir)
