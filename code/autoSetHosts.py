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
import getIpRange
import pingIp
import selectHost

if os.name!='posix':
    print 'Sorry, we just support Linux/Unix now!'
    sys.exit(0)

if __name__=='__main__':
    getIpRange.getIpRange()
    pingIp.pingIp()
    selectHost.select()
