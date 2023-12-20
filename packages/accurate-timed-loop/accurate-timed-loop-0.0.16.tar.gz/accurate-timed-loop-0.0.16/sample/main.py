import datetime
import random
import sys
import time

import math
from on_the_fly_stats import OTFStats

import accurate_timed_loop


# --------------------
## sample run of the loop calculating average timing error
class Sample:

    # --------------------
    ## run a loop approximately 100 times and
    # calculate the average error per loop
    #
    # @return None
    def run(self):
        loop_delay = 0.250  # seconds
        total_wait = loop_delay * 100  # do 100 loops

        # expected time
        expected = 0

        # the adjustment value
        # adj = 0.0  # no adjustment
        if sys.platform == 'darwin':
            adj = 0.008925  # macos
        elif sys.platform == 'linux':
            adj = 0.004839  # ubu
        else:
            adj = 0.014216  # win msys2

        stats = OTFStats()
        stats.create_average('avg1')
        stats.create_min_max('mm1')
        stats.create_stddev('sd1')

        print(f'{"": >3} {"expected": >10} {"elapsed": >10} {"diff1(ms)": >10} {"actual(s)": >10} {"diff2(ms)": >10}')
        for elapsed, start_time in accurate_timed_loop.accurate_wait(total_wait, loop_delay, fixed_adjustment=adj):
            # this is the actual loop time from the time the loop was started to now
            actual = datetime.datetime.now().timestamp() - start_time
            # the difference between the value returned from accurate_wait vs the expected time
            diff1 = (elapsed - expected) * 1000
            # the difference between the actual time vs the expected time
            diff2 = (actual - expected) * 1000
            stats.update_min_max('mm1', diff2)
            stats.update_average('avg1', math.fabs(diff2))
            stats.update_stddev('sd1', math.fabs(diff2))

            print(f'{stats.min_max["mm1"].num_elements: >3} {expected: >10.6f} {elapsed: >10.6f} '
                  f'{diff1: >10.3f} {actual: >10.6f} {diff2: >10.3f}')

            # the expected time at the top of the next loop
            expected += loop_delay

            # simulate some random activity
            time.sleep(random.uniform(0, loop_delay + 0.01))

        # show some stats
        print('\n')
        print('Stats:')
        print(f'loop count     : {stats.min_max["mm1"].num_elements: >3} loops')
        print(f'Error Range    : {stats.min_max["mm1"].minimum: >1.3f} to {stats.min_max["mm1"].maximum: >1.3f} mS')
        print(f'Error Stddev   : {stats.stddev["sd1"].stddev: >10.3f} mS')
        print(f'Error Average  : {stats.average["avg1"].average: >10.3f} mS')
        adj = (math.fabs(stats.min_max["mm1"].minimum) + math.fabs(stats.min_max["mm1"].maximum)) / 2.0
        print(f'Recommended adj: {adj / 1000.0: >1.6f}')


# --------------------
def main():
    sample = Sample()
    sample.run()


# --------------------
main()
