#!/usr/bin/env python3

import datetime
import serial
import sys
from xml.etree.cElementTree import fromstring

serial = serial.Serial('/dev/ttyUSB0', 57600)

try:
    while True:
        msg = serial.readline()
        if not msg:
            raise ValueError('Time out')

        print(msg)

        xml = fromstring(msg)

        if xml.tag != 'msg':
            continue

        if xml.find('hist'):
            continue

        watts = int(xml.find('ch1').find('watts').text)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        print(timestamp, watts)

except KeyboardInterrupt:
    sys.exit()
