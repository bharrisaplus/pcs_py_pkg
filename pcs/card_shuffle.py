''' Shuffle a deck of cards and produce the decklist '''

import random
import os

from ._constants import card_num_to_name as lookup_card
from ._utils import _setup_52
from .gui import CloseUp


class CardShuffle:
    '''A lean mean card shuffling machine

    Attributes:
        card_pool (list[tuple(str, int)]): The cards to randomize. See _constants.py@_setup_52
        position_pool (list[int]): The potential numbered spots cards can be placed in
        position_count (int): The number of positions
        mixed_cards (list[tuple(str, int)]): see card_pool
        last_cut_position (int|None): Where the last cut was made
    '''

    def __init__(self):
        self.card_pool, self.position_pool = _setup_52()
        self.position_count = len(self.position_pool)
        self.mixed_cards = [0] * self.position_count
        self.last_cut_position = None

    def shuffle_cards(self):
        '''Randomize the order of given cards and place at random in a new deck

        Having a bank of cards and positions, pick a random card from both banks for a new order.
        '''

        random_cards = random.sample(population=self.card_pool, k=len(self.card_pool))
        random_positions = random.sample(population=self.position_pool, k=self.position_count)

        for _ in range(self.position_count):
            card_to_place = random_cards[random.randrange(len(random_cards))]
            position_to_use = random_positions[random.randrange(len(random_positions))]

            self.mixed_cards[position_to_use] = card_to_place

            random_cards.remove(card_to_place)
            random_positions.remove(position_to_use)

    def maybe_cut(self, is_arbitrary=False):
        '''Rearrange the deck at a determined point

        From the determined point take every card before the point and move it to the back of
            the list. The determined point can be picked by:
                * arbitrary: index from one of 1-3 randomly selected cards from the deck
                * peapod: index of card found next to new deck order neighbor

        Args:
            is_arbitrary (bool): See above (default: `False`)
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

                if info[0] == previous_info[0] and (
                    info[1] == previous_info[1] - 1 or
                    info[1] == previous_info[1] + 1
                ):
                    cut_position = idx_info
                    break

                previous_info = info

        if cut_position:
            self.mixed_cards = self.mixed_cards[cut_position:] + self.mixed_cards[:cut_position]

        self.last_cut_position = cut_position

    def cards_as_text(self):
        """ Create plain-text output of the card order

        Looks like: [ "1) Jack of Spade", "2) Four of Club" ]

        Returns:
            list[str]: See description above.
        """

        card_catalog = []

        for card_catalog_idx, card_stuff in enumerate(self.mixed_cards, start=1):
            card_catalog.append("{}) {} of {}".format(
                card_catalog_idx,
                lookup_card.get(card_stuff[1]).capitalize(),
                card_stuff[0].capitalize()
            ))

        return card_catalog

    def display_decklist_in_console(self, to_file=False):
        '''Output card order to the screen and maybe a file.

        Args:
            to_file (bool): Whether or not to create a file. (default: `False`)
        '''

        card_roll = self.cards_as_text()

        print(*card_roll, sep="\n")

        if to_file:
            file_descriptor = os.open('shuffled.decklist.txt', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

            with os.fdopen(file_descriptor, mode='w') as out_file:
                out_file.write("\n".join(card_roll))

            print("\nDecklist written to 'shuffled.decklist.txt'.")

    def ndo_example(self):
        ''' Print cards in new deck order: (♠️:A-K, ♦️:A-K, ♣️:K-A, ♥️:K-A) '''

        pad = CloseUp(window_title="pcs: ndo", screen_grab_filename="ndo")

        pad.load_cards(self.card_pool, color_per_suite=True)
        pad.show_window()

    def display_decklist_in_gui(self, four_color=False):
        '''Show the shuffled cards using utf-8 symbols

        Args:
            four_color (bool): Whether to use one color pre suite (default: False)
        '''

        pad = CloseUp(window_title="pcs: pseudo card shuffle")

        pad.load_cards(self.mixed_cards, color_per_suite=four_color)
        pad.show_window()


def card_shuffle(cut_deck=False, arbitrary_cut=False):
    ''' Shortcut to quickly get a random list of cards '''

    dealer = CardShuffle()

    dealer.shuffle_cards()

    if cut_deck:
        dealer.maybe_cut(is_arbitrary=arbitrary_cut)

    return dealer.cards_as_text()
