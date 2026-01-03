# Run like python -m tool.test_runner -h

import argparse
import unittest
import sys

from spec import shape_spec
from spec import metric_spec
from spec import behavior_spec
from spec import widget_spec

if __name__ == '__main__':
    testRunnerParser = argparse.ArgumentParser(prog="tool.test_runner",
        description="Run specific test(s) for pcs."
    )

    testRunnerParser.add_argument("-b", "--behavior", action="store_true",
        help="Run tests for checking how app handles inputs"
    )

    testRunnerParser.add_argument("-s", "--shape", action="store_true",
        help="Run tests for checking app output"
    )

    testRunnerParser.add_argument("-m", "--metric", action="store_true",
        help="Run tests for checking randomness of app output"
    )

    testRunnerParser.add_argument("-w", "--widget", action="store_true",
        help="Run tests for verifying the correct information is passed to the gui"
    )

    if len(sys.argv) > 1:
        testRunnerArgs = testRunnerParser.parse_args()
        testGroup = unittest.TestSuite()
        testGroupRunner = unittest.TextTestRunner()

        if testRunnerArgs.shape:
            testGroup.addTest(shape_spec.ShapeCheck('test_sham'))

        if testRunnerArgs.behavior:
            testGroup.addTest(behavior_spec.BehaviorCheck('test_sham'))

        if testRunnerArgs.metric:
            testGroup.addTest(metric_spec.MetricCheck('test_jaro'))
            testGroup.addTest(metric_spec.MetricCheck('test_peapod'))

        if testRunnerArgs.widget:
            testGroup.addTest(widget_spec.WidgetCheck('test_sham'))

        testGroupRunner.run(testGroup)
    else:
        print("No options passed.")
