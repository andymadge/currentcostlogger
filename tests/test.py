# -*- coding: utf-8 -*-

import unittest

import sys
import os
from xml.etree.cElementTree import fromstring

# Ensure we import the dev module not an installed version of it
# (see https://github.com/kennethreitz/samplemod/commit/48f4c8dba40cb2fe03a74a7a4d7d979892601ddc)
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Add tests folder to path, so we can import any helper modules from that folder:
tests_dirs = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, tests_dirs)

# then import the module(s) you're testing
from currentcost import *

sample_msg_0 = '''2019-01-09T21:05:30Z,,<msg><src>CC128-v1.29</src><dsb>02628</dsb><time>21:05:14</time><tmpr>24.3</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>01397</watts></ch1></msg>'''

sample_msg_1 = '''2019-01-09T21:34:22Z,Dishwasher,<msg><src>CC128-v1.29</src><dsb>02628</dsb><time>21:34:06</time><tmpr>24.5</tmpr><sensor>1</sensor><id>02773</id><type>1</type><ch1><watts>02197</watts></ch1></msg>'''

class TestStuff(unittest.TestCase):
    """Test the currentcost module"""

    def test_extract_values(self):
        """Confirm extraction works"""
        msg = sample_msg_0.split(',')[2]
        xml = fromstring(msg)
        watts, temperature = extract_values(xml)
        self.assertEqual((1397, "24.3"), (watts, temperature))

    def test_format_line_sensor_0(self):
        """Check output for sensor 0, second field should be empty"""
        # this is not a very good test since it depends on the current time
        line = format_line("the_data", 0)
        self.assertEqual(line, "{},,the_data".format(now_timestamp()))

    def test_format_line_sensor_1(self):
        """Check output for sensor 1, second field should contain IAM name"""
        # this is not a very good test since it depends on the current time
        # also it actually tests multiple functions rather than just 1
        os.environ['IAM_NAME'] = "Nursery123"
        line = format_line("the_data", 1)
        self.assertEqual(line, "{},Nursery123,the_data".format(now_timestamp()))


if __name__ == '__main__':
    unittest.main()
