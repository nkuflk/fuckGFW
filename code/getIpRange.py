#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: getIpRange.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-25 15:00:10
#########################################################################

import os
import re

def getIpRange():
    cmd = os.popen('nslookup -q=TXT _netblocks.google.com 8.8.8.8')
    output = cmd.read()
    pattern = re.compile(r'ip4:(.*?)/')
    match = pattern.findall(output)
    fileHandle = open('googleIpRange', 'w')
    for line in match:
        fileHandle.write(line+'\n')
    fileHandle.close()
    return match
