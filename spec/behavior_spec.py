import unittest
from unittest.mock import patch
import json
from types import SimpleNamespace

import pcs.command_line as PCSCLI

class BehaviorCheck(unittest.TestCase):
    def setUp(self):
        self.args_json = '{"write": false, "gui": false, "four_color": false, "ndo": false, "cut": false, "arbitrary": false}'


    def test_sham(self):
        # something like the populated namespace from argparse.ArgumentParser.parse_args()
        mock_args = json.loads(self.args_json, object_hook=lambda dct: SimpleNamespace(**dct))

        self.assertEqual(mock_args.write, False, "Nothing to see here yet")
        self.assertEqual(mock_args.gui, False, "Nothing to see here yet")
        self.assertEqual(mock_args.four_color, False, "Nothing to see here yet")
        self.assertEqual(mock_args.ndo, False, "Nothing to see here yet")
        self.assertEqual(mock_args.cut, False, "Nothing to see here yet")
        self.assertEqual(mock_args.arbitrary, False, "Nothing to see here yet")
