import unittest

import tool.stats as CardShuffleStats

class MetricCheck(unittest.TestCase):
    def test_jaro(self):
        ex_a = ['F','A','R','M','V','I','L','L','E']
        ex_b = ['F','A','R','E','M','V','I','E','L']
        solution = CardShuffleStats.get_jaro_edit_distance_from(ex_b, ex_a)

        self.assertEqual(0.8842592592592592, solution[0],
            "jaro similarity between {} and {} should be 0.8842592592592592".format(ex_a, ex_b)
        )

        self.assertEqual(len(solution[1][0]), 8,
            "matched characters in {} and {} should be 8".format(ex_a, ex_b)
        )

        self.assertEqual(len(solution[1][1]), 8,
            "matched characters in {} and {} should be 8".format(ex_a, ex_b)
        )

        self.assertEqual(solution[2], 2/2,
            "transpositions counted in {} and {} should be 1".format(ex_a, ex_b)
        )

    def test_jaro_again(self):
        ex_c = ['H','E','L','L','O']
        ex_d = ['H','E','Y','Y','A']
        solution = CardShuffleStats.get_jaro_edit_distance_from(ex_c, ex_d)

        self.assertEqual(1.8/3, solution[0],
            "jaro similarity between {} and {} should be 0.6".format(ex_c, ex_d)
        )

        self.assertEqual(len(solution[1][0]), 2,
            "matched characters in {} and {} should be 2".format(ex_c, ex_d)
        )

        self.assertEqual(len(solution[1][1]), 2,
            "matched characters in {} and {} should be 2".format(ex_c, ex_d)
        )

        self.assertEqual(solution[2], 0,
            "transpositions counted in {} and {} should be 0".format(ex_c, ex_d)
        )

    def test_jaro_again_again(self):
        ex_e = ['X','L','N','G','X','A','T','C','X','R']
        ex_f = ['F','Y','J','L','H','D','R','Q','D','M']
        solution = CardShuffleStats.get_jaro_edit_distance_from(ex_e, ex_f)

        self.assertEqual(abs(1.4/3), solution[0],
            "jaro edit distance between {} and {} should be ~0.4667".format(ex_e, ex_f)
        )

        self.assertEqual(len(solution[1][0]), 2,
            "matched characters in {} should be 2".format(ex_e)
        )

        self.assertEqual(len(solution[1][1]), 2,
            "matched characters in {} should be 2".format(ex_f)
        )

        self.assertEqual(solution[2], 0,
            "transpositions counted in {} and {} should be 0".format(ex_e, ex_f)
        )

    def test_peapod(self):
        ex_g = [16,18,13,15,11,12,14,10,17]
        ex_h = [10,11,12,13,14,15,16,17,18]

        solution = CardShuffleStats.count_peapods_from(ex_g, ex_h)

        self.assertEqual(solution[0], 1, "Should be 1 ripe peapod in {}".format(ex_g))
        self.assertEqual(solution[1], 15, "Should be 15 green peapods in {}".format(ex_h))

    def test_peapod_agin(self):
        ex_i = [24,25,19,18,23,21,22,26,20]
        ex_j = [18,19,20,21,22,23,24,25,26]

        solution = CardShuffleStats.count_peapods_from(ex_i, ex_j)

        self.assertEqual(solution[0], 3, "Should be 3 ripe peapods in {}".format(ex_i))
        self.assertEqual(solution[1], 13, "Should be 13 green peapods in {}".format(ex_j))

    def test_peapod_again_again(self):
        ex_k = [6,2,4,1,7,5,8,3]
        ex_l = [1,2,3,4,5,6,7,8]

        solution = CardShuffleStats.count_peapods_from(ex_k, ex_l)

        self.assertEqual(solution[0], 0, "Should be 0 ripe peapods in {}".format(ex_k))
        self.assertEqual(solution[1], 14, "Should be 13 green peapods in {}".format(ex_l))
