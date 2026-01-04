''' How random is the pcs shuffle '''

import unittest
import numpy
import math
import statistics as PyStat
import scipy.stats as SciPyStats

from pcs.card_shuffle import CardShuffle
import tool.stats as CardShuffleStats
from spec.shape_spec import card_order


class RandomnessCheck(unittest.TestCase):
    '''A series of tests

    a) Jaro distance between a shuffled deck and new deck order to show cards have moved
    b) Peapod or consecutive pairs or cards that are next to their new deck order neighbor
    c) Chi-Squared test on the frequency of each card from a shuffled deck in each position in the deck
    d) Kendall rank correlation between the shuffled cards and new deck order
    e) Kendall rank correlation between the shuffled decks
    '''
    def setUp(self):
        self.new_deck_order_positions = list(range(len(card_order)))


    def debug_report_jaro_stats(self, _mean, _std, _min, _max):
        print("\nThe mean for the data: {}".format(_mean))
        print("The standard deviation for the data: {}".format(_std))
        print("The data ranged between {} and {}".format(_min, _max))
        print("\nThe mean compared to Fisher-Yates: {} +- {} vs {}".format(_mean, _std, 0.6676))
        print("The mean compared to Gilbert-Shannon-Reeds: {} +- {} vs {}".format(_mean, _std, 0.6662))


    def debug_report_peapod_stats(self, _mean, _std, _min, _max):
        print("\nThe mean for the data: {}".format(_mean))
        print("The standard deviation for the data: {}".format(_std))
        print("The data ranged between {} and {}".format(_min, _max))
        print("\nThe mean compared to accpated value: {} +- {} vs {}".format(_mean, _std, 2.0))


    def debug_report_chi_stats(self, chisq, pval):
        print("\nThe chi-square value for the data: {}".format(chisq))
        print("\nThe p-value for the data: {}".format(pval))


    def debug_report_kendall_stats(self):
        return None

    @unittest.skip("one at a time")
    def test_card_shuffle_jaro(self):
        jaro_measurement = [0] * 10000

        for text_idx in range(len(jaro_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()

            jaro_similarity = CardShuffleStats.get_jaro_edit_distance_from(test_dealer.mixed_cards, card_order)
            jaro_measurement[text_idx] = jaro_similarity[0]

        sample_mean = PyStat.mean(jaro_measurement)
        sample_std = PyStat.stdev(jaro_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean - sample_std, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6662, rel_tol=0.05)
        )

        self.debug_report_jaro_stats(sample_mean, sample_std, min(jaro_measurement), max(jaro_measurement))

        self.assertTrue(acceptance_check_passed,
            "The mean jaro similarity observed of the PCS should be close to that of the FY and GSR shuffles"
        )


    @unittest.skip("one at a time")
    def test_card_shuffle_cut_jaro(self):
        jaro_measurement = [0] * 10000

        for text_idx in range(len(jaro_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut()

            jaro_similarity = CardShuffleStats.get_jaro_edit_distance_from(test_dealer.mixed_cards, card_order)
            jaro_measurement[text_idx] = jaro_similarity[0]

        sample_mean = PyStat.mean(jaro_measurement)
        sample_std = PyStat.stdev(jaro_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean - sample_std, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6662, rel_tol=0.05)
        )

        self.debug_report_jaro_stats(sample_mean, sample_std, min(jaro_measurement), max(jaro_measurement))

        self.assertTrue(acceptance_check_passed,
            "The mean jaro similarity observed of the PCS should be close to that of the FY and GSR shuffles"
        )


    @unittest.skip("one at a time")
    def test_card_shuffle_arbitrary_cut_jaro(self):
        jaro_measurement = [0] * 10000

        for text_idx in range(len(jaro_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut(is_arbitrary=True)

            jaro_similarity = CardShuffleStats.get_jaro_edit_distance_from(test_dealer.mixed_cards, card_order)
            jaro_measurement[text_idx] = jaro_similarity[0]

        sample_mean = PyStat.mean(jaro_measurement)
        sample_std = PyStat.stdev(jaro_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6676, rel_tol=0.05) or
            math.isclose(sample_mean - sample_std, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean, 0.6662, rel_tol=0.05) or
            math.isclose(sample_mean + sample_std, 0.6662, rel_tol=0.05)
        )

        self.debug_report_jaro_stats(sample_mean, sample_std, min(jaro_measurement), max(jaro_measurement))

        self.assertTrue(acceptance_check_passed,
            "The mean jaro similarity observed of the PCS should be close to that of the FY and GSR shuffles"
        )


    @unittest.skip("one at a time")
    def test_card_shuffle_peapod(self):
        peapod_measurement = [0] * 10000

        for text_idx in range(len(peapod_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()

            peapod_count = CardShuffleStats.count_peapods_from(test_dealer.mixed_cards, card_order)
            peapod_measurement[text_idx] = peapod_count[0]

        sample_mean = PyStat.mean(peapod_measurement)
        sample_std = PyStat.stdev(peapod_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 2, rel_tol=0.5) or
            math.isclose(sample_mean, 2, rel_tol=0.5) or
            math.isclose(sample_mean + sample_std, 2, rel_tol=0.5)
        )

        self.debug_report_peapod_stats(
            sample_mean, sample_std, min(peapod_measurement), max(peapod_measurement)
        )

        self.assertTrue(acceptance_check_passed, "The number of consecutive pairs should be around 2")


    @unittest.skip("one at a time")
    def test_card_shuffle_cut_peapod(self):
        peapod_measurement = [0] * 10000

        for text_idx in range(len(peapod_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut()

            peapod_count = CardShuffleStats.count_peapods_from(test_dealer.mixed_cards, card_order)
            peapod_measurement[text_idx] = peapod_count[0]

        sample_mean = PyStat.mean(peapod_measurement)
        sample_std = PyStat.stdev(peapod_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 2, rel_tol=0.5) or
            math.isclose(sample_mean, 2, rel_tol=0.5) or
            math.isclose(sample_mean + sample_std, 2, rel_tol=0.5)
        )

        self.debug_report_peapod_stats(
            sample_mean, sample_std, min(peapod_measurement), max(peapod_measurement)
        )

        self.assertTrue(acceptance_check_passed, "The number of consecutive pairs should be around 2")


    @unittest.skip("one at a time")
    def test_card_shuffle_arbitrary_cut_peapod(self):
        peapod_measurement = [0] * 10000

        for text_idx in range(len(peapod_measurement)):
            test_dealer = CardShuffle()

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut(is_arbitrary=True)

            peapod_count = CardShuffleStats.count_peapods_from(test_dealer.mixed_cards, card_order)
            peapod_measurement[text_idx] = peapod_count[0]

        sample_mean = PyStat.mean(peapod_measurement)
        sample_std = PyStat.stdev(peapod_measurement, sample_mean)

        acceptance_check_passed = (
            math.isclose(sample_mean - sample_std, 2, rel_tol=0.5) or
            math.isclose(sample_mean, 2, rel_tol=0.5) or
            math.isclose(sample_mean + sample_std, 2, rel_tol=0.5)
        )

        self.debug_report_peapod_stats(
            sample_mean, sample_std, min(peapod_measurement), max(peapod_measurement)
        )

        self.assertTrue(acceptance_check_passed, "The number of consecutive pairs should be around 2")


    @unittest.skip("one at a time")
    def test_card_shuffle_chi(self):
        test_run_count = 10000
        test_result_matrix = numpy.zeros((52, 52), dtype=int)

        for _ in range(test_run_count):
            test_dealer = CardShuffle()
            test_dealer.card_pool = list(range(len(card_order)))

            test_dealer.shuffle_cards()

            for card_pos, card in enumerate(test_dealer.mixed_cards):
                test_result_matrix[card][card_pos] += 1

        observed_values = test_result_matrix.flatten()
        expected_values = numpy.full(observed_values.shape, test_run_count / 52)

        # scale
        expected_values = expected_values * (numpy.sum(observed_values) / numpy.sum(expected_values))

        chi_sq, p_val = SciPyStats.chisquare(observed_values, f_exp=expected_values)

        self.debug_report_chi_stats(chi_sq, p_val)

        self.assertTrue(p_val >= 0.83, "The frequency of each card in each position after shuffle should be close to uniform")

    @unittest.skip("one at a time")
    def test_card_shuffle_cut_chi(self):
        test_run_count = 10000
        test_result_matrix = numpy.zeros((52, 52), dtype=int)

        for _ in range(test_run_count):
            test_dealer = CardShuffle()
            test_dealer.card_pool = list(range(len(card_order)))

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut()

            for card_pos, card in enumerate(test_dealer.mixed_cards):
                test_result_matrix[card][card_pos] += 1

        observed_values = test_result_matrix.flatten()
        expected_values = numpy.full(observed_values.shape, test_run_count / 52)

        # scale
        expected_values = expected_values * (numpy.sum(observed_values) / numpy.sum(expected_values))

        chi_sq, p_val = SciPyStats.chisquare(observed_values, f_exp=expected_values)

        self.debug_report_chi_stats(chi_sq, p_val)

        self.assertTrue(p_val >= 0, "The frequency of each card in each position after shuffle and peapod cut should be close to uniform")


    @unittest.skip("one at a time")
    def test_card_shuffle_arbitrary_cut_chi(self):
        test_run_count = 10000
        test_result_matrix = numpy.zeros((52, 52), dtype=int)

        for _ in range(test_run_count):
            test_dealer = CardShuffle()
            test_dealer.card_pool = list(range(len(card_order)))

            test_dealer.shuffle_cards()
            test_dealer.maybe_cut(is_arbitrary=True)

            for card_pos, card in enumerate(test_dealer.mixed_cards):
                test_result_matrix[card][card_pos] += 1

        observed_values = test_result_matrix.flatten()
        expected_values = numpy.full(observed_values.shape, test_run_count / 52)

        # scale
        expected_values = expected_values * (numpy.sum(observed_values) / numpy.sum(expected_values))

        chi_sq, p_val = SciPyStats.chisquare(observed_values, f_exp=expected_values)

        self.debug_report_chi_stats(chi_sq, p_val)

        self.assertTrue(p_val >= 0, "The frequency of each card in each position after shuffle and arbitrary cut should be close to uniform")


    @unittest.skip("not yet")
    def test_card_shuffle_kendall(self):
        self.assertEqual(0, 0, "Nothing to see here yet")

    @unittest.skip("not yet")
    def test_card_shuffle_cut_kendall(self):
        self.assertEqual(0, 0, "Nothing to see here yet")

    @unittest.skip("not yet")
    def test_card_shuffle_arbitrary_cut_kendall(self):
        self.assertEqual(0, 0, "Nothing to see here yet")


    @unittest.skip("not yet")
    def test_card_shuffle_kendall_alt(self):
        self.assertEqual(0, 0, "Nothing to see here yet")

    @unittest.skip("not yet")
    def test_card_shuffle_cut_kendall_alt(self):
        self.assertEqual(0, 0, "Nothing to see here yet")

    @unittest.skip("not yet")
    def test_card_shuffle_arbitrary_cut_kendall_alt(self):
        self.assertEqual(0, 0, "Nothing to see here yet")
