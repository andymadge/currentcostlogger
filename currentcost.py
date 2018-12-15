#!/usr/bin/env python3

import datetime
import serial
import sys
from xml.etree.cElementTree import fromstring

serial = serial.Serial('/dev/ttyUSB0', 57600)

def read_serial(serial):
    msg = serial.readline().decode('utf-8', errors='ignore').rstrip()
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
        # f.write(data)
        print(now_timestamp(), data, file=f)

def now_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

def process_xml(xml, msg):
        sensor = int(xml.find('sensor').text)

        write_datafile(msg, sensor)

        watts, temperature = extract_values(xml)

        timestamp = now_timestamp()

        # print(timestamp, watts, temperature)

def main():
    while True:
        try:
            msg = read_serial(serial)
            xml = fromstring(msg)

            if xml.tag != 'msg':
                continue

            if xml.find('hist'):
                data = xml.find('hist').find('data')
                tag = data[1].tag
                # print(data[1].tag, data[1].text)
                if tag[0] == 'h':
                    # hourly history
                    write_datafile(msg, "hist_hourly")
                elif tag[0] == 'd':
                    # daily history
                    write_datafile(msg, "hist_daily")
                elif tag[0] == 'm':
                    # monthly history
                    write_datafile(msg, "hist_monthly")
                continue
            
            process_xml(xml, msg)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
