Altered Panda
=============

Entry in PyWeek #13  <http://www.pyweek.org/13/>
URL: http://www.pyweek.org/e/teamstrong/
Team: teamstrong
Members: rozifus, danaran, jtrain
License: see LICENSE.txt


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------

Move the cursor around the screen with the mouse.


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

Acknowlegments
--------------

We use Kytten for the menu system: Accessed http://code.google.com/p/kytten/

