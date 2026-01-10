''' Shuffle a deck of cards and produce the decklist '''

import random
import os
import supports_color

from ._utils import (
    _setup_52,
    get_card_title,
    get_card_color
)

from .gui import CloseUp

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
console_card_colors: list[str] = ['\033[36m', '\033[31m', '\033[32m', '\033[33m']
console_color_reset: str = '\033[0m'


class CardShuffle:
    '''A lean mean card shuffling machine

    Attributes:
        card_pool (list[int]): The cards to randomize. See _utils.py@_setup_52
        position_pool (list[int]): The potential numbered spots cards can be placed in
        position_count (int): The number of positions
        mixed_cards (list[int]): see card_pool
        last_cut_position (int|None): Where the last cut was made
    '''

    def __init__(self):
        self.card_pool, self.position_pool = _setup_52()
        self.position_count = len(self.position_pool)
        self.mixed_cards = [0] * self.position_count
        self.last_cut_position = None


    def shuffle_cards(self) -> None:
        '''Randomize the order of given cards and place at random in a new deck

        Having a bank of both cards and positions, for each position pick a random card and
            a random position from their respective banks to create a new order.
        '''

        random_cards = random.sample(population=self.card_pool, k=len(self.card_pool))
        random_positions = random.sample(population=self.position_pool, k=self.position_count)

        for _ in range(self.position_count):
            card_to_place = random_cards[random.randrange(len(random_cards))]
            position_to_use = random_positions[random.randrange(len(random_positions))]

            self.mixed_cards[position_to_use] = card_to_place

            random_cards.remove(card_to_place)
            random_positions.remove(position_to_use)

    def maybe_cut(self, is_arbitrary: bool = False) -> None:
        '''Rearrange the deck at a determined point

        From the determined point take every card before the point and move it to the back of
            the list. The determined point can be picked by:
                * arbitrary: index from one of 1-3 randomly selected cards from the deck
                * peapod: index of card found next to new deck order neighbor
        '''

        cut_position = None

        if is_arbitrary:
            possible_cut = random.sample(population=self.mixed_cards, k=random.randrange(1, 4))
            cut_position = self.mixed_cards.index(random.sample(possible_cut, k=1)[0])

        else:
            previous_info = None

            for idx_info, info in enumerate(self.mixed_cards):
                if previous_info is None:
                    previous_info = info
                    continue

                if abs(previous_info - info) == 1:
                    cut_position = idx_info
                    break

                previous_info = info

        if cut_position:
            self.mixed_cards = self.mixed_cards[cut_position:] + self.mixed_cards[:cut_position]

        self.last_cut_position = cut_position

    def cards_as_text(self, four_color: bool = False) -> tuple[list[int], list[int]]:
        """ Create plain-text output of the card order
    
        Looks like: [ "1) Jack of Spade", "2) Four of Club" ]

        The card order can optionally include color using ANSI escape codes
        """

        for_console = []
        for_file = []

        for card_catalog_idx, card_stuff in enumerate(self.mixed_cards, start=1):
            _line ="{}) {}".format(card_catalog_idx, get_card_title(card_stuff))

            if four_color and supports_color.supportsColor.stdout:
                for_console.append("{}{}{}".format(
                    console_card_colors[get_card_color(card_stuff, four_color=True)],
                    _line, console_color_reset
                ))
            else:
                for_console.append(_line)

            for_file.append(_line)

        return for_console, for_file

    def display_decklist_in_console(self, to_file: bool = False, four_color: bool = False) -> None:
        ''' Output card order to the screen and maybe a file '''

        console_catalog, file_catalog = self.cards_as_text(four_color=four_color)

        print(*console_catalog, sep="\n")

        if to_file:
            file_descriptor = os.open('shuffled.decklist.txt', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

            with os.fdopen(file_descriptor, mode='w') as out_file:
                out_file.write("\n".join(file_catalog))

            print("\nDecklist written to 'shuffled.decklist.txt'.")

    def ndo_example(self) -> None:
        ''' Print cards in new deck order: (♠️:A-K, ♦️:A-K, ♣️:K-A, ♥️:K-A) '''

        pad = CloseUp(window_title="pcs: ndo", screen_grab_filename="ndo")

        pad.load_cards(self.card_pool, color_per_suite=True)
        pad.show_window()

    def display_decklist_in_gui(self, four_color: bool = False) -> None:
        ''' Show the shuffled cards using utf-8 symbols '''

        pad = CloseUp(window_title="pcs: pseudo card shuffle")

        pad.load_cards(self.mixed_cards, color_per_suite=four_color)
        pad.show_window()


def card_shuffle(cut_deck: bool = False, arbitrary_cut: bool = False) -> list[str]:
    ''' Shortcut to quickly get a random list of cards '''

    dealer = CardShuffle()

    dealer.shuffle_cards()

    if cut_deck:
        dealer.maybe_cut(is_arbitrary=arbitrary_cut)

    return dealer.cards_as_text()
