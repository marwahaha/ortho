ortho
=====

Application ludique pour enfants pour répéter des mots d'orthographe. Ecrit en python avec wxPython.

Principe de l'application
-------------------------

Des mots sont énoncé par l'application, l'élève doit les écrire sans faute. Des mots peuvent facilement être rajoutés, il suffit de rajouter les fichiers son (.wav) dans le bon répertoire.

Deux modes sont sont disponibles:  

 -  le mode interrogation où la correction est réalisée à la fin des mots (le nombre de mots par interro est configurable).
 -  le mode entrainement où toute erreur est immédiatement signalée à l'élève afin qu'il puisse se corriger de suite.
 
 
Comment installer et démarrer l'application?
--------------------------------------------

L'application fonctionne sous Linux et sous Windows.

### Linux

Au préalable, il faut avoir installé: python, python-wxgtk2.8 ("wxPython") et pygame.
Sous Debian et Ubuntu, la commande suivante installe ces dépendances:

    apt-get install python python-wxgtk2.8 python-pygame

Pour lancer l'application, il suffit de cliquer sur le fichier `launch_ortho.py`, ou de lancer dans un terminal:

    python launch_ortho.py

### Windows

Il faut installer:

* [Python](http://www.python.org)
* [wxPython](http://www.wxpython.org)

Pour lancer l'application, il faut exécuter dans un terminal: `python launch_ortho.py`.


TODO
----

 * Augmenter la base de mots
 * Proposer une méthode d'installation pour simple pour Linux et Windows. 
   - Windows: peut-être convertir le script en un exécutable?
   - Linux: proposer un packet `.deb`
 * Idée: explorer si le principe de l'application ne peut pas être intégré dans une autre application existante, telle que [gcompris](http://www.gcompris.net)