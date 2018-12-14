#!/usr/bin/env python3

import datetime
import serial
import sys
from xml.etree.cElementTree import fromstring

serial = serial.Serial('/dev/ttyUSB0', 57600)

def read_serial(serial):
    msg = serial.readline()
    if not msg:
        raise ValueError('Time out')
    print(msg)
    return msg

def extract_values(xml):
    watts = int(xml.find('ch1').find('watts').text)
    temperature = xml.find('tmpr').text
    return watts, temperature

def write_datafile(data, sensor):
    with open("data_sensor_{}.xml".format(sensor), "a") as f:
        f.write(data.decode('utf-8'))

def process_xml(xml, msg):
        sensor = int(xml.find('sensor').text)

        if sensor == 0:
            # whole-house data
            write_datafile(msg, sensor)
        elif sensor == 1:
            # IAM 1
            write_datafile(msg, sensor)

        watts, temperature = extract_values(xml)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        print(timestamp, watts, temperature)

def main():
    try:
        while True:
            msg = read_serial(serial)
            xml = fromstring(msg)

            if xml.tag != 'msg':
                continue

            if xml.find('hist'):
                # TODO: Write history here
                continue

            process_xml(xml, msg)

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
