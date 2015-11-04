#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: pingIp.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-26 11:20:39
#########################################################################

import nmap
import threading
import pycurl
import re
import os

import ipRange

outFile = open('output', 'w')

class PingThread(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.loss = 0
        self.avg = 0
        self.domain = ''

    def run(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip,'443')
        flag = False
        try:
            if nm[self.ip].has_tcp(443):
                if nm[self.ip]['tcp'][443]['state']=='open':
                    flag = True
        except:
            pass
        if flag:
            try:
                c = pycurl.Curl()
                c.setopt(pycurl.URL, 'https://'+self.ip)
                c.perform()
            except Exception, e:
                e = str(e)
                pattern = re.compile(r'name \((.*)\) does')
                match = pattern.findall(e)
                if len(match)==0:
                    return
                self.domain = match[0]
            cmd = 'ping -c5 -w5 '+self.ip
            result = os.popen(cmd,'r').read().strip()
            pattern = re.compile(r'received, (.*) packet loss')
            match = pattern.findall(result)
            if len(match)==0:
                return
            self.loss = match[0]
            pattern = re.compile(r' = .*/(.*)/.*/.*')
            match = pattern.findall(result)
            if len(match)==0:
                return
            self.avg = match[0]
            outFile.write(self.ip+' ')
            outFile.write(self.loss+' ')
            outFile.write(self.avg+' ')
            outFile.write(self.domain+'\n')

def pingIp():
    ipList = ipRange.getIpList()
    for ip in ipList:
        ipPrev = '.'.join(ip[:-1])
        threads = [PingThread(ipPrev+'.'+str(x)) for x in range(1,255)]
    #    else:
    #        for i in range(0,256):
    #            threads[i].start()
    #        for i in range(0,256):
    #            threads[i].join()

if __name__=='__main__':
    pingIp()
    outFile.close()
