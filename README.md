<h1> Boxweeper </h1>

This is an open-source implementation of a game
similar to the popular Windows game minesweeper.

This game is implemented in Python version 3.10 and
uses flask to create a dynamic 3D representation of
a box system displayed on a web browser.

<h1>Installing flask</h1>
This game is available for MacOS and Windows
though up to the release of this README.md it
has only been operated on MacOS.

To get started you must have Python installed
and if you don't have flask installed you can
enter in terminal or Command Prompt:

pip3.10 install flask

<h1>How to Play</h1>
The goal of the game is to label all the mines and then
hit the confirmation button.
If you got all of them then you win, otherwise you
continue finding them.

How to find the mines.

Each cube has 26 mines around it
9 below, 9 above, and 8 directly beside
when a cube is clicked on it will display
a number on it displaying the amount of mines
touching it.
It is by comparing the different amount of mines
surrounding each cube that you narrow down where
the mines are located.

If you click on a mine then you get a warning
saying strike. Two more clicks on any mine and 
you lose.

When a cube is narrowed down to possibly be a mine
it should be labeled for the game to check later.

The way to label the mines is to right click on them
which will color them black, and then click on them
to make sure they stay marked.

<h1> Customization </h1>
When running the game by opening terminal or 
command-prompt and executing the python script
Head_Script.py, 

the browser on localhost
(port is found at the bottom inside Head_Script.py)
will display an html form requesting which mode
to play on.

Mode #0 customizes the view size and the puzzle size.

Modes 1 - 3 constrain the view to 3 by 3 by 3 but allow the selection of the entire puzzle size.

Mode 1 doesn't tint the image based on position.

Mode 2-3 buttons do get tinted based on position.

Mode 2 makes selected blocks invisible if they have no mines around them.

Mode 3 makes selected blocks inscribed with 0 if they have no mines around them.

Finally all modes start with a block button inscribed with 0 to start off.

<h1>Credits</h1>

Credits to my two brothers for redesigning the button that becomes
most of the game content found in unclicked.png (can be changed if desired).

<h1>Contributions</h1>
Contributions and suggestions are welcome,
feel free to make a pull request or contact me at 
matthieu.r.hart@gmail.com

