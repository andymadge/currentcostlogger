CurrentCost Logger
===

This is a simple python script that runs continuously and reads the data from the CurrentCost Energy Monitor on the serial port.

It adds a timestamp and saves the data to daily text files, separated by sensor.  For simplicity, the output is basically CSV, but the last of the fields contains the raw XML from the monitor.

It can also save the history data, but this is currently commented out since I have no use for it.

I am then using Filebeat to send the data to Logstash, which in turn routes to both Elasticsearch and EmonCMS.

It can be run directly on the local computer, or it can be run in a Docker container.

This was originally based on MIT licensed https://github.com/tomtaylor/currentcost but modified a lot.


Local Deployment
---
1. Install PySerial `pip3 install pyserial` or even better with pipenv `pipenv3 install pyserial`
2. Run the script `./currentcost.py`

It will write datafiles in the `data` subfolder.


Docker Deployment
---
1. Install Docker(!) and docker-compose
2. Clone this repo and cd to the repo folder
3. Type `docker-compose up`

The `data` folder is bind-mounted in the container, so the data will be written there, as for local deployment.

Troubleshooting
---

If you get error:

    serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0'

This means you don't have permissons on the serial device.  You can check this with `ls -l`:

    andym@docker:~$ ls -l /dev/ttyUSB0
    crw-rw---- 1 root dialout 188, 0 Dec 15 10:37 /dev/ttyUSB0

Therefore you need to be either root, or in the `dialout` group to access the port.

Add yourself to the group like this:

    sudo adduser $USER dialout

or

    sudo usermod -aG dialout $USER

You may need to log out and back in for the group membership to take effect