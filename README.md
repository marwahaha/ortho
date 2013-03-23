ortho
=====

This is a educational application for children within 6 to 12 years old.  The goal is to help the kid to learn the spelling of new words. 

The application is written in python and uses wxPython.

Application's principles
------------------------

The application dictates words, the kid has to type it correctly. New words can easily be added by copying new sound files (.wav) within the appropriate folder.

The application has two way of working:
 - the quiz mode: the correction is performed at the end of the quiz (the number of word per quiz is configurable).
 - the training mode: any mistake is directly reported to the user, so that he can correct himself on the spot.
 
How to install and start the application?
-----------------------------------------

The application runs on Linux and Windows.

### Linux

python, python-wxgtk2.8 ("wxPython") and pygame must be installed.
For Debian and Ubuntu, the following command installs the dependencies:

    apt-get install python python-wxgtk2.8 python-pygame

To run the application, simply click on the file `launch_ortho.py`, or launch in a terminal:

    python launch_ortho.py

### Windows

First, install: 

* [Python](http://www.python.org)
* [wxPython](http://www.wxpython.org)

To run the application, execute in a terminal: `python launch_ortho.py`.


TODO
----

 * Log files: 1 debug log and one parental (or teacher) log ("application log")
 * when changing the lessons or the mode, "reset" the interface and the state of the application
 * at the end of an interrogation, list the correct words in the textpanel
 * When closing the application, display a specific window with score & faults
 * TECHOS: enhance the way the lessons are managed in GuiGlue
 * TECHOS: why on Linux, the menu bar is not showing up at the start of the application?
 * Add new words
 * Facilitate the installation on Linux and Windows:
   - Windows: convert the script into an executable?
   - Linux: create a package `.deb`
 * Idea: explore whether the application can be integrated within an existing educational suite, like [gcompris](http://www.gcompris.net)
