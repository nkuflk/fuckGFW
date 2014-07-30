#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: selectHost.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-30 16:47:38
#########################################################################

domains = ["*.google.com",
        "accounts.google.com",
        "checkout.google.com",
        "adwords.google.com",
        "mail.google.com",
        "*.mail.google.com",
        "*.googleusercontent.com",
        "*.gstatic.com",
        "*.googleapis.com",
        "*.appspot.com",
        "*.googlecode.com",
        "*.google-analytics.com",
        "ssl.google-analytics.com"]

def select():
    dicts = {}
    hosts = []
    fileHandle = open('output', 'r')
    value = 0
    for line in fileHandle:
        temp = line.split(' ')
        temp[3] = temp[3].strip()
        if dicts.has_key(temp[3]):
            tempvalue = dicts[temp[3]]
            if (int)(temp[1][:-1])<hosts[tempvalue][1]:
                hosts[tempvalue][0] = temp[0]
                hosts[tempvalue][1] = (int)(temp[1][:-1])
                hosts[tempvalue][2] = (float)(temp[2])
            elif (int)(temp[1][:-1])==hosts[tempvalue][1]:
                if (float)(temp[2])<hosts[tempvalue][2]:
                    hosts[tempvalue][0] = temp[0]
                    hosts[tempvalue][1] = (int)(temp[1][:-1])
                    hosts[tempvalue][2] = (float)(temp[2])
        else:
            if temp[3] in domains:
                dicts[temp[3]] = value
                hosts.append([temp[0],(int)(temp[1][:-1]),(float)(temp[2]),temp[3]])
                value = value+1
    return hosts

if __name__=='__main__':
    hosts = select()
