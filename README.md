Installation
---
1. Install PySerial `pip3 install pyserial` or even better with pipenv `pipenv3 install pyserial`
2. Run the script `./currentcost.py`

It will write xml datafiles in the same folder.


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