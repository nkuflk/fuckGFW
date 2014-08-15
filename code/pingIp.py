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

outFile = open('output', 'w')

class pingThread(threading.Thread):

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

def getIpList():
    ip = []
    fileHandle = open('googleIpRange', 'r')
    for line in fileHandle:
        ip.append(line)
    fileHandle.close()
    ipList = [[0]*4]*len(ip)
    lineId = 0
    for line in ip:
        temp = line.split('.')
        temp[3] = temp[3].strip()
        ipList[lineId] = temp
        lineId = lineId + 1
    return ipList

def pingIp():
    ipList = getIpList()
    for k in range(0,len(ipList)):
        if ipList[k][2]=='0':
            for j in range(60,256):
                tmp = str(ipList[k][0])+'.'+str(ipList[k][1])+'.'+str(j)
                print tmp
                threads = []
                for i in range(0,256):
                    ip = tmp+'.'+str(i)
                    threads.append(pingThread(ip))
                for i in range(0,256):
                    threads[i].start()
                for i in range(0,256):
                    threads[i].join()
        else:
            tmp = str(ipList[k][0])+'.'+str(ipList[k][1])+'.'+str(ipList[k][2])
            print tmp
            threads = []
            for i in range(0,256):
                ip = tmp+'.'+str(i)
                threads.append(pingThread(ip))
            for i in range(0,256):
                threads[i].start()
            for i in range(0,256):
                threads[i].join()

if __name__=='__main__':
    pingIp()
    outFile.close()
