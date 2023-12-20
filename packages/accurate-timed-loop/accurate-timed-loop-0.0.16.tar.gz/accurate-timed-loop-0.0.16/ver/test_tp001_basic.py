import datetime
import random
import sys
import time
import unittest

import math
from pytest_ver import pth

from tools import loader

loader.loader_init()

# pylint: disable=wrong-import-order
from on_the_fly_stats import OTFStats  # pylint: disable=wrong-import-position
import accurate_timed_loop  # pylint: disable=wrong-import-position


# -------------------
class TestTp001(unittest.TestCase):

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        pass

    # --------------------
    @classmethod
    def tearDownClass(cls):
        pth.term()

    # --------------------
    def test_tp_001_basic(self):
        pth.proto.protocol('tp-001', 'basic calls')

        pth.proto.step('verify initial values')

        stats = OTFStats()
        stats.create_average('avg1')
        stats.create_min_max('mm1')
        stats.create_stddev('sd1')

        if sys.platform == 'darwin':
            adj = 0.008925  # macos
        elif sys.platform == 'linux':
            adj = 0.004839  # ubu
        else:
            adj = 0.009849  # win msys2

        pth.proto.step('verify accuracy')
        expected = 0
        total_wait = 10
        loop_delay = 0.100
        for _, start_time in accurate_timed_loop.accurate_wait(total_wait, loop_delay, fixed_adjustment=adj):
            actual = datetime.datetime.now().timestamp() - start_time
            diff = math.fabs(actual - expected) * 1000  # ms
            stats.update_average('avg1', diff)
            stats.update_stddev('sd1', diff)
            diff2 = (actual - expected) * 1000  # ms
            stats.update_min_max('mm1', diff2)

            expected += loop_delay
            # introduce random sleep to simulate other executing within this loop
            time.sleep(random.uniform(0, loop_delay + 0.01))

        # the values are in mS
        print(f'{"num loops": <15}: {stats.average["avg1"].num_elements: >10}')
        print(f'{"average diff": <15}: {stats.average["avg1"].average: >10.3f} mS')
        print(f'{"std dev diff": <15}: {stats.stddev["sd1"].stddev: >10.3f} mS')
        print(f'{"minimum diff": <15}: {stats.min_max["mm1"].minimum: >10.3f} mS')
        print(f'{"maximum diff": <15}: {stats.min_max["mm1"].maximum: >10.3f} mS')

        pth.ver.verify_delta(int(total_wait / loop_delay), stats.average['avg1'].num_elements, 2, reqids=['SRS-001'])

        # Note: in the maximum is greater than 30ms, then there will be a failure in various stats
        # Note: this assumes that the adj value has been adjusted to minimize the error

        # the average discrepancy from the requested loop_delay time is better than +/- 6mS
        pth.ver.verify_delta(0.0, stats.average['avg1'].average, 6.0, reqids=['SRS-001'])
        # the std dev shows that 95% of all discrepancies is better than  +/- 12mS
        pth.ver.verify_delta(0.0, stats.stddev['sd1'].stddev, 6.0, reqids=['SRS-003'])

        # the min and max values of the discrepancy is better than +/- 30mS
        pth.ver.verify_ge(stats.min_max['mm1'].minimum, -30.0, reqids=['SRS-002'])
        pth.ver.verify_le(stats.min_max['mm1'].maximum, 30.0, reqids=['SRS-002'])
