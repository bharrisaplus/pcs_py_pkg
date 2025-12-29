# (P)seudo (C)ard (S)huffler - python package
For producing a pseudo-randomized list of playing cards (♠️♦️♣️♥️).

* [Overview](#overview)
* [Install](#install)
  - [pypi](#pypi)
    + [pip](#pip)
    + [pipx](pipx)
  - [uv](#uv)
* [Usage](#usage)
  - [Package](#package)
  - [CLI](#cli)
    + [Text output only](#console-output-only)
    + [Writing to a file](#writing-to-file)
    + [Graphic output](#gui-output)
    + [NDO Example](#ndo)
    + [Help display](#help-display)

## Overview
Shuffling by taking a random sampling from the available cards and placing them in a position based on a random sampling from available positions in the deck.

## Install
### pypi
---
#### pip
```
$ python -m pip install pcs
```
#### pipx
```
$ pipx install pcs
```
### uv
---
```
$ uv tool install pcs
```
## Usage
Outputs the list of cards to the console and optionally to a file.

### Package
---
With the package installed:
```
# some_file.py
from pcs import CardShuffle, card_shuffle # OR import pcs

dealer = CardShuffle() # OR pcs.CardShuffle

dealer.shuffle_cards()

print(dealer.cards_text())

shuffled_cards = card_shuffle() # OR pcs.card_shuffle

print(shuffled_cards)


```

### CLI
---
#### Console output only
```
$ python -m pcs
1) Two of Spade
....
52) Queen of Heart

# OR

$ pipx pcs
1) Two of Spade
....
52) Queen of Heart

# OR

$ uvx pcs
1) Two of Spade
....
52) Queen of Heart
```

#### Writing to file
```
$ python -m pcs [-w,--write]
1) Three of Club
....
52) Five of Heart
Decklist written to 'shuffled.decklist.txt'.

# OR

$ pipx pcs [-w,--write]
1) Three of Club
....
52) Five of Heart
Decklist written to 'shuffled.decklist.txt'.

# OR

$ uvx pcs [-w,--write]
1) Three of Club
....
52) Five of Heart
Decklist written to 'shuffled.decklist.txt'.
```

### GUI output
---
```
$ python -m pcs [-g,--gui]

# OR

$ pipx pcs [-g,--gui]

# OR

$ uvx pcs [-g,--gui]
```

#### NDO Example
```
$ python -m pcs [-n, --ndo]

# OR

$ pipx pcs [-n, --ndo]

# OR

$ uvx pcs [-n, --ndo]
```

### Help display
---
```
$ python card_shuffle.py -h
usage: card_shuffle.py [-h] [-w] [-g] [-n] [-c] [-a]

Producing a pseudo-randomized list of playing cards.

options:
  -h, --help       show this help message and exit
  -w, --write      Flag to set for writing output to a text file
  -g, --gui        Flag to set for displaying output using tkinter
  -n, --ndo        Flag to set for displaying demo using tkinter. Other options are ignored when set.
  -c, --cut        Flag to set for cutting the deck after the shuffle at a consecutive pair if found.
  -a, --arbitrary  Flag to set for cutting the deck after the shuffle at a random spot.

# OR

$ pipx pcs -h

# OR 

# uvx pcs -h
```