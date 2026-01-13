==========================
(P)seudo (C)ard (S)huffler
==========================
For producing a pseudo-randomized list of playing cards (♠️♦️♣️♥️).

.. contents:: Table of Contents
   :depth: 2
   :local:

Install
=======

.. code-block:: bash


   $ python -m pip install pcs
   $ pipx install pcs

Usage
=====
Outputs the list of cards to the console and optionally to a file.

Package
-------
.. code-block:: python


   from pcs import CardShuffle, card_shuffle
   import pcs
   
   dealer = CardShuffle() # OR pcs.CardShuffle
   
   dealer.shuffle_cards()
   
   print(dealer.cards_text())
   print(card_shuffle())
   print(pcs.card_shuffle())

CLI
---
.. code-block:: bash

   $ pcs -h
   usage: card_shuffle.py [-h] [-w] [-g] [-n] [-c] [-a]
   
   Producing a pseudo-randomized list of playing cards.
   
   options:
    -h, --help       show this help message and exit
    -w, --write      Flag to set for writing output to a text file
    -g, --gui        Flag to set for displaying output using tkinter
    -n, --ndo        Flag to set for displaying demo using tkinter. Other options are ignored when set.
    -c, --cut        Flag to set for cutting the deck after the shuffle at a consecutive pair if found.
    -a, --arbitrary  Flag to set for cutting the deck after the shuffle at a random spot.
