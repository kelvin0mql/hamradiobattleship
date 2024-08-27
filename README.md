# Battleship Game for Ham Radio

Welcome to the classic game of Battleship, reimagined for a fun Amateur Radio activity.

## Installation

Before playing, make sure that you have Python installed in your system. This game has been tested with Python 3.7+.

Once Python is installed, simply clone this repository and navigate to the repository's root directory in a terminal window.
To run the game, type:
`python battleship.py`

## Game Setup

It is assumed you'll use Dropbox to "publish" the current Hit/Miss/Sunk status of your board. After all, in a Ham Radio
activity, you might be part way through a game when the bands shift and you lose contact with your opponent. While that
can be frustrating, this is also part of *the point* of this version of the game. You can pick up instead with another
opponent, so long as each of you can grab a copy of each other's shared/published file named:

`battleship-{callsign}.txt`

If you're not using Dropbox, you may want to adjust this script to use other means, be that OneDrive, GoogleDrive, or
whatever. In an event with many active players, it will be important for whatever method you choose be something that
can keep that file current "out there". But if you're just going to play one-on-one, starting with a blank grid for
both players is the norm.

So, whomever your opponent/s is/are, you will copy (or create) a file named: 

`battleship-{callsign].txt` in your home directory for your opponent. If manually created, using a plain text editor, 
make 10 rows of 10 lower-case "b" characters, like this...

```bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
bbbbbbbbbb
```
That's the starting grid.

When you start it (assuming there is no `battleship-{callsign}_private.txt` file in your home directory), you'll 
be asked for your callsign, and a new game board will be created for you to play. Otherwise, your 
previous game board(s) will load.

The game board consists of a 10x10 grid where each cell can occupy one of four states:

- `b`: Ocean (light blue)
- `m`: Missed shot (white - also for pending, while waiting for your opponent to tell you "Hit" or "Miss")
- `h`: Hit on a ship (red)
- `s`: Sunk ship (black)

An uppercase letter denotes the player's own ships. You'll be seeing these only in

`battleship-{yourCallSign}_private.txt`.

## How to Play

Use your mouse to interact with the game:

- **Left click**: Changes the state of a cell. It cycles from Ocean -> Miss -> Hit -> Sink -> Ocean.
- **Right click**: Places or removes a ship.

(Note: once you've placed a ship icon in a cell, then the first click won't go white, but instead skip to red.)

When a ship is placed, the letter turns to upper-case in your _private.txt file, and an anchor icon appears. Only do this
on the left-hand grid - this is your "Defensive Grid". If you right-click again, the anchor will disappear, and the
letter will drop to lower-case in your _private.txt file. 

Note: On Mac OS X, it will probably be middle-click instead of right-click, for inexplicable reasons.

Note: The changes you make on your board will be directly reflected on a public board which is viewable to any new 
opponent who downlaods it. However, your ships will appear as `b` in the public board, effectively hiding them.

### Saving The Game

The game state is automatically saved to text files whenever you make changes on the grids. You can find these files at
your home directory, and your Dropbox directory, like this...
```Kelvins-Mac-mini:~ kelvind$ ls -l ba*txt;ls -l Dropbox/ba*txt
-rw-r--r--@ 1 kelvind  staff  110 Aug 27 14:06 battleship-AAA.txt
-rw-r--r--@ 1 kelvind  staff  110 Aug 27 14:06 battleship-BBB.txt
-rw-r--r--  1 kelvind  staff  110 Aug 27 14:05 battleship-N0MQL_private.txt
-rw-r--r--@ 1 kelvind  staff  110 Aug 27 14:05 Dropbox/battleship-N0MQL.txt
Kelvins-Mac-mini:~ kelvind$ 
```

### Resetting The Board

If you wish to reset a grid at any point, click on the 'Reset' button. This clears that entire grid, allowing you to 
start afresh.

## Ham Event Rule Suggestions

Score points for completing salvos, where a Miss is one point, a Hit is 3 points, and sinking different sized ships are
different amounts of bonus points. Switch modes and bands for multipliers. e.g. Complete salvos on 20m Phone, then on
JS8Call, then on Olivia, then on CW... = x4 multipliers. Drop to 40m and do all 4 modes again, another x4. Consider 
trying to complete a few salvos on Feld Hell! How 'bout PSK? RTTY, Contestia... see how many of the obscure modes in
fldigi you can use to declare ultimate naval victory!!
