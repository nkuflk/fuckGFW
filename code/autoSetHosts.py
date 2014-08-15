#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: setHosts.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-25 09:14:37
#########################################################################

import sys
import os

if os.name!='posix':
    print 'Sorry, we just support Linux/Unix now!'
    sys.exit(0)

if __name__=='__main__':
    fileHandle = open('/etc/hosts', 'r')
    temp = ''
    for line in fileHandle:
        temp += line
    temp += '\n'
    fileHandle.close()
    fileHandle = open('hosts.bak', 'r')
    for line in fileHandle:
        temp += line
    fileHandle.close()
    os.rename('/etc/hosts','/etc/hosts.myHosts')
    fileHandle = open('/etc/hosts', 'w')
    fileHandle.write(temp)
    fileHandle.close()
