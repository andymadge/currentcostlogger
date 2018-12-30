#!/usr/bin/env python3

import datetime
import serial
import sys
import os
from xml.etree.cElementTree import fromstring

def read_serial(ser):
    msg = ser.readline().decode('utf-8', errors='ignore').rstrip()
    if not msg:
        raise ValueError('Time out')
    print(now_timestamp(), msg)
    return msg

def extract_values(xml):
    watts = int(xml.find('ch1').find('watts').text)
    temperature = xml.find('tmpr').text
    return watts, temperature

def format_line(data, sensor, iam=""):
    if sensor > 0:
        iam = get_iam_name()
    line = "{},{},{}".format(now_timestamp(), iam, data)
    return line

def get_iam_name():
    iam = os.getenv('IAM_NAME', "")
    return iam

def write_datafile(data, sensor):
    fname = "sensor_{}_{}.xml".format(sensor, date_today())
    fname = os.path.join("data", fname)
    # print(fname)
    with open(fname, "a") as f:
        # f.write(data)

        print(format_line(data, sensor), file=f)

def now_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

def date_today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def process_xml(xml, msg):
    sensor = int(xml.find('sensor').text)

    write_datafile(msg, sensor)

    timestamp = now_timestamp()

    # watts, temperature = extract_values(xml)
    # print(timestamp, watts, temperature)

def main():
    ser = serial.Serial('/dev/ttyUSB0', 57600)
    while True:
        try:
            msg = read_serial(ser)
            xml = fromstring(msg)

            if xml.tag != 'msg':
                continue

            if xml.find('hist'):
                # # This is commented out since I have no useful way to display it
                # data = xml.find('hist').find('data')
                # tag = data[1].tag
                # # print(data[1].tag, data[1].text)
                # if tag[0] == 'h':
                #     # hourly history
                #     write_datafile(msg, "hist_hourly")
                # elif tag[0] == 'd':
                #     # daily history
                #     write_datafile(msg, "hist_daily")
                # elif tag[0] == 'm':
                #     # monthly history
                #     write_datafile(msg, "hist_monthly")
                continue
            
            process_xml(xml, msg)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
