#!/usr/bin/env python3
# simple script to provide some info on local system CPU usage
#

import os
import sys
import subprocess

#from datetime import datetime
#import pprint
#import glob

# -----------------------------------------------------------------------------
# main()
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    """ Run /usr/bin/sar -P ALL along with an optional day # to get CPU usage
    """

    flag = ''
    minusage = 90.0
    maxusage = 10.0

    if len(sys.argv) > 1:
        daystr = sys.argv[1]
        flag = ['-f', '/var/log/sa/sa' + sys.argv[1]]

    cmdline = ['/usr/bin/sar', '-P', 'ALL']
    if len(flag) > 1:
        cmdline += flag

    work = subprocess.check_output(cmdline, stderr=subprocess.STDOUT).decode('utf-8')
    lines = work.split('\n')
    for line in lines:
        if 'Linux' in line:
            parts = line.split()
            datestamp = parts[3]
            # take the base system name, delete the '(':
            sysname   = parts[2].split('.')[0].strip('(')
            continue

        if 'CPU' in line or 'all' in line or len(line) == 0 or 'Average' in line:
            continue

        parts = line.split()
        # do a list comprehension:
        hour, minute, seconds = [int(x) for x in parts[0].split(':')]

        if parts[1] == 'AM' and hour == 12:
            hour = 0

        if parts[1] == 'PM' and hour != 12:
            hour += 12

        timestr = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)
        idle = 100 - float(parts[8]);
        if idle > maxusage:
           print(datestamp, timestr, sysname, 'CPU', parts[2], 'usage:', str(round(idle, 2)) + '%')


        continue

# EOF:
