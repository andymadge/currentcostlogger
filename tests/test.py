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

sample_msg_0 = '''<msg><src>CC128-v1.29</src><dsb>02616</dsb><time>23:45:32</time><tmpr>23.6</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>00750</watts></ch1></msg>'''

sample_msg_1 = '''<msg><src>CC128-v1.29</src><dsb>02616</dsb><time>23:45:30</time><tmpr>23.7</tmpr><sensor>1</sensor><id>02773</id><type>1</type><ch1><watts>00000</watts></ch1></msg>'''

class TestStuff(unittest.TestCase):
    """Test the currentcost module"""

    def test_extract_values(self):
        """Confirm extraction works"""
        xml = fromstring(sample_msg_0)
        watts, temperature = extract_values(xml)
        self.assertEqual((750, "23.6"), (watts, temperature))

    def test_format_line(self):
        """Confirm extraction works"""
        # this is not a very good test since it depends on the current time
        line = format_line(sample_msg_0)
        self.assertEqual(line, "{timestamp} {data}".format(
            timestamp=now_timestamp(), data=sample_msg_0))


if __name__ == '__main__':
    unittest.main()
