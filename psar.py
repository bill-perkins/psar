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
    """
    """
    flag = ['', '']
    minusage = 90.0

    if len(sys.argv) > 1:
        daystr = sys.argv[1]
        flag = ['-f', '/var/log/sa/sa' + sys.argv[1]]

    cmdline = ['/usr/bin/sar', '-P', 'ALL']
    if flag[0] == '-f':
        cmdline.append(flag[0])
        cmdline.append(flag[1])

    work = subprocess.check_output(cmdline, stderr=subprocess.STDOUT)
    work = work.decode('utf-8') # change from bytes to string
    lines = work.split('\n')
    print(len(lines), 'lines')
    for line in lines:
        if 'CPU' in line or 'all' in line or len(line) == 0 or 'Average' in line:
            continue

        parts = line.split()
        # 00:00:00
        h, m, s = parts[0].split(':')
        hour    = int(h)
        minute  = int(m)
        seconds = int(s)
        if parts[1] == 'AM' and hour == 12:
            hour = 0
        if parts[1] == 'PM' and hour != 12:
            hour += 12

        timestr = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(seconds).zfill(2)
        idle = float(parts[8]);
        if idle < minusage:
           print(timestr, 'idle:', parts[8] + '%')


        continue

# EOF:
