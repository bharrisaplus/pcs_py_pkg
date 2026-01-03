''' Helpful methods for card shuffling '''

from PIL import ImageGrab

from ._constants import (
    suites as card_suites,
    number_values as card_nums
)


def _setup_52():
    '''Arrange playing cards in new deck order (♠️:A-K, ♦️:A-K, ♣️:K-A, ♥️:K-A).

    Returns:
        (tuple[ tuple(str, int)], list[int] ]): The arranged cards and the positions to fill in:
            * tuple(str, int): model representing the cards
                * str: The suite of the card. See card_shuffle_constants.py:suites
                * int: The number value of the card. See card_shuffle_constants.py:number_values
            * list[int]: The numbered spots where cards can go
    '''

    card_bank = []

    for suite in card_suites:
        if suite in card_suites[:2]:
            for idx in card_nums:
                card_bank.append((suite, idx))
        else:
            for idx in reversed(card_nums):
                card_bank.append((suite, idx))

    return card_bank, list(range(len(card_bank)))


def _capture_tkinter(capture_bounds, capture_prefix='shuffled'):
    '''Save an image of the display cards

    Grab the current screen using pillow and crop the area outside of the gui

    Args:
        capture_bounds (tuple[int, int, int, int]): Coordinates for crop
        capture_prefix (str): What to name the saved file (default: 'shuffled')
    '''

    capture_filename = "{}.decklist.png".format(capture_prefix)
    capture_image = ImageGrab.grab(bbox=capture_bounds)

    capture_image.save(capture_filename)
    print("Decklist saved to '{}'".format(capture_filename))
