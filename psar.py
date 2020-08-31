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

    cmdline = ['/usr/bin/sar', '-P', 'ALL']

    if len(sys.argv) > 1:
        cmdline += ['-f', '/var/log/sa/sa' + sys.argv[1]]


    work = subprocess.check_output(cmdline, stderr=subprocess.STDOUT).decode('utf-8')
    lines = work.split('\n')
    lines.reverse()
    print('date,time,system,', end='')

    line = lines.pop()
    if 'Linux' in line:
        parts = line.split()

        # get the datestamp:
        datestamp = parts[3]

        # take the base system name, delete the '(':
        sysname   = parts[2].split('.')[0].strip('(').strip(')')

        # get the cpu count:
        cpucount  = int(parts[5].split()[0].strip('('))
    else:
        print('file format error: first line should start with "Linux"')
        sys.exit(1)

    for i in range(cpucount - 1):
        print('CPU', i, 'usage,', end='')

    print('CPU', i + 1, 'usage')

    while len(lines) > 0:
        line = lines.pop()
        # got header info, skip stuff we don't care about:
        if len(line) == 0 or 'CPU' in line or 'all' in line or 'Average' in line or 'Linux' in line:
            continue

        # the line has '%idle' in it; get all of them:
        parts = line.split()
        # do a list comprehension:
        hour, minute, seconds = [int(x) for x in parts[0].split(':')]

        if parts[1] == 'AM' and hour == 12:
            hour = 0

        if parts[1] == 'PM' and hour != 12:
            hour += 12

        timestr = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)
        print(datestamp + ',' + timestr + ',' + sysname + ',', end='')

        for i in range(cpucount):
            parts = line.split()
            idle = 100 - float(parts[8]);
            if i < cpucount - 1:
                print(str(round(idle, 2)) + '%,', end='')
            else:
                print(str(round(idle, 2)) + '%')

            line = lines.pop()

# EOF:
