''' Console interface to shuffle cards '''
import argparse

import pcs


def go() -> None:
    '''Start the program

    options:
        -h, --help
        -w, --write
        -g, --gui
        -n, --ndo
        -c, --cut
        -a, --arbitrary
    '''
    cardShuffleParser = argparse.ArgumentParser(prog="pcs",
        description="Producing a pseudo-randomized list of playing cards."
    )

    cardShuffleParser.add_argument("-w", "--write", action="store_true",
        help="Flag to set for writing output to a text file"
    )

    cardShuffleParser.add_argument("-g", "--gui", action="store_true",
        help="Flag to set for displaying output using tkinter"
    )

    cardShuffleParser.add_argument("-f", "--four-color", action="store_true",
        help="Flag to set for displaying each suite in a unique color in the tkinter gui window")

    cardShuffleParser.add_argument("-n", "--ndo", action="store_true",
        help="Flag to set for displaying demo using tkinter. Other options are ignored when set."
    )

    cardShuffleParser.add_argument("-c", "--cut", action="store_true",
        help="Flag to set for cutting the deck after the shuffle at a consecutive pair if found."
    )

    cardShuffleParser.add_argument("-a", "--arbitrary", action="store_true",
        help="Flag to set for cutting the deck after the shuffle at a random spot."
    )

    cardShuffleArgs = cardShuffleParser.parse_args()
    dealer = pcs.CardShuffle()

    if cardShuffleArgs.ndo:
        dealer.ndo_example()

    else:
        # Get a blank deck and mix it up

        dealer.shuffle_cards()

        if cardShuffleArgs.cut:
            dealer.maybe_cut(is_arbitrary=cardShuffleArgs.arbitrary)

            if dealer.last_cut_position:
                print("Cut deck @ {}".format(dealer.last_cut_position))

        # Show the cards

        dealer.display_decklist_in_console(to_file=cardShuffleArgs.write, four_color=cardShuffleArgs.four_color)

        if cardShuffleArgs.gui:
            dealer.display_decklist_in_gui(four_color=cardShuffleArgs.four_color)


if __name__ == '__main__':
    go()
