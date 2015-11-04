#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: getIpRange.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-26 09:00:10
#########################################################################

import re
import dns.resolver

def getIpList():
    answers = dns.resolver.query('_netblocks.google.com', 'TXT')
    pattern = re.compile(r'ip4:(.*?)/')
    match = pattern.findall(str(answers[0]))
    return filter(lambda x : x[2]!='0', [line.split('.') for line in match])
