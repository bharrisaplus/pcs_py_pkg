import unittest
import re

import pcs._utils as PCSUtils
from pcs.card_shuffle import (
    CardShuffle,
    console_card_colors
)

class ShapeCheck(unittest.TestCase):
    def test_get_card_name(self):
        expected_1 = ["ace of spade", "ace of diamond", "ace of club", "ace of heart"]
        solution_1 = PCSUtils.get_card_title(0)
        solution_2 = PCSUtils.get_card_title(13)
        solution_3 = PCSUtils.get_card_title(38)
        solution_4 = PCSUtils.get_card_title(51)
        expected_2 = ["king of spade", "king of diamond", "king of club", "king of heart"]
        solution_5 = PCSUtils.get_card_title(12)
        solution_6 = PCSUtils.get_card_title(25)
        solution_7 = PCSUtils.get_card_title(26)
        solution_8 = PCSUtils.get_card_title(39)

        self.assertEqual([solution_1, solution_2, solution_3, solution_4], expected_1,
            "The title of a card should be retrieved based on the ndo position of the card"
        )

        self.assertEqual([solution_5, solution_6, solution_7, solution_8], expected_2,
            "The title of a card should be retrieved based on the ndo position of the card"
        )


    def test_get_card_symbol(self):
        expected_1 = [ '🂡', '🃁', '🃑', '🂱' ]
        solution_1 = PCSUtils.get_card_symbol(0)
        solution_2 = PCSUtils.get_card_symbol(13)
        solution_3 = PCSUtils.get_card_symbol(38)
        solution_4 = PCSUtils.get_card_symbol(51)
        expected_2 = [ '🂮', '🃎', '🃞', '🂾' ]
        solution_5 = PCSUtils.get_card_symbol(12)
        solution_6 = PCSUtils.get_card_symbol(25)
        solution_7 = PCSUtils.get_card_symbol(26)
        solution_8 = PCSUtils.get_card_symbol(39)

        self.assertEqual([solution_1, solution_2, solution_3, solution_4], expected_1,
            "The symbol of a card should be retrieved based on the ndo position of the card"
        )

        self.assertEqual([solution_5, solution_6, solution_7, solution_8], expected_2,
            "The symbol of a card should be retrieved based on the ndo position of the card"
        )


    def test_get_card_color(self):
        expected_1 = [0,1,0,1]
        solution_1 = PCSUtils.get_card_color(0)
        solution_2 = PCSUtils.get_card_color(13)
        solution_3 = PCSUtils.get_card_color(38)
        solution_4 = PCSUtils.get_card_color(51)
        solution_5 = PCSUtils.get_card_color(12)
        solution_6 = PCSUtils.get_card_color(25)
        solution_7 = PCSUtils.get_card_color(26)
        solution_8 = PCSUtils.get_card_color(39)
        expected_2 = [0,1,2,3]
        solution_9 = PCSUtils.get_card_color(0, four_color=True)
        solution_10 = PCSUtils.get_card_color(13, four_color=True)
        solution_11 = PCSUtils.get_card_color(38, four_color=True)
        solution_12 = PCSUtils.get_card_color(51, four_color=True)
        solution_13 = PCSUtils.get_card_color(12, four_color=True)
        solution_14 = PCSUtils.get_card_color(25, four_color=True)
        solution_15 = PCSUtils.get_card_color(26, four_color=True)
        solution_16 = PCSUtils.get_card_color(39, four_color=True)

        self.assertEqual([solution_1, solution_2, solution_3, solution_4], expected_1,
            "The color of a card should be retrieved based on the ndo position of the card"
        )

        self.assertEqual([solution_5, solution_6, solution_7, solution_8], expected_1,
            "The color of a card should be retrieved based on the ndo position of the card"
        )

        self.assertEqual([solution_9, solution_10, solution_11, solution_12], expected_2,
            "The color of a card should be retrieved based on the ndo position of the card"
        )


    def test_cards_as_text(self):
        test_rgx = r"^((5)([0-2])|([1-4]?)([0-9]{1}))\)\s((ace)|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)|(ten)|(jack)|(queen)|(king))\sof\s((spade)|(diamond)|(club)|(heart))$"
        card_order = list(range(52))
        test_dealer = CardShuffle()
        
        test_dealer.shuffle_cards()

        cards_for_console, cards_for_file = test_dealer.cards_as_text()
        ccards_for_console, ccards_for_file = test_dealer.cards_as_text(four_color=True)
        maybe_color_card_text = ccards_for_console[0]

        self.assertEqual(len(cards_for_console), len(cards_for_file),"The lines of text should match the number of cards")
        self.assertRegex(cards_for_console[0], test_rgx, "The lines of text should match regex")
        self.assertRegex(cards_for_file[0], test_rgx, "The lines of text should match regex")
        self.assertRegex(ccards_for_file[0], test_rgx, "The lines of text should match regex")
        self.assertTrue(any(x in maybe_color_card_text for x in console_card_colors), "The text should contain color")


    def test_shuffle(self):
        card_order = list(range(52))
        test_dealer = CardShuffle()
        
        test_dealer.shuffle_cards()

        self.assertEqual(len(test_dealer.mixed_cards), len(card_order),
            "The shuffled deck should retain the same number of cards as before the shuffle"
        )

        self.assertNotEqual(test_dealer.mixed_cards, card_order,
            "The shuffled deck should not be the same as new deck order"
        )


    def test_cut(self):
        swear_mix = [25,9,1,41,7,46,39,43,5,11,2,4,13,22,6,34,35,28,21,14,19,50,10,3,15,0,42,40,44,33,12,26,48,31,37,20,8,30,23,32,49,17,27,45,36,51,47,18,29,38,16,24]
        swear_cut = [35,28,21,14,19,50,10,3,15,0,42,40,44,33,12,26,48,31,37,20,8,30,23,32,49,17,27,45,36,51,47,18,29,38,16,24,25,9,1,41,7,46,39,43,5,11,2,4,13,22,6,34]
        test_dealer = CardShuffle()
        test_dealer.mixed_cards = swear_mix

        test_dealer.maybe_cut()

        self.assertEqual(len(test_dealer.mixed_cards), len(swear_mix),
            "The peapod cut deck should retain the same number of cards as before the cut"
        )

        self.assertEqual(swear_mix.index(test_dealer.mixed_cards[0]), swear_mix.index(swear_cut[0]),
            "The peapod cut deck should be cut at the first consecutive pair"
        )


    def test_cut_arbitrary(self):
        swear_mix = [25,9,1,41,7,46,39,43,5,11,2,4,13,22,6,34,35,28,21,14,19,50,10,3,15,0,42,40,44,33,12,26,48,31,37,20,8,30,23,32,49,17,27,45,36,51,47,18,29,38,16,24]
        test_dealer = CardShuffle()
        test_dealer.mixed_cards = swear_mix

        test_dealer.maybe_cut(is_arbitrary=True)
        
        solution = test_dealer.mixed_cards

        self.assertEqual(len(solution), len(swear_mix),
            "The arbitrary cut deck should retain the same number of cards as before the cut"
        )

        self.assertEqual(solution[0], swear_mix[test_dealer.last_cut_position],
            "The arbitrary cut deck should be cut somwhere in the deck"
        )
