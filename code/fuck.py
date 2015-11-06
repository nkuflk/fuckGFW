#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: fuck.py
# Author: nkuflk
# mail: nkuflk@gmail.com
# Created Time: 2014-07-26 11:20:39
#########################################################################

import subprocess
import socket
import threading
import Queue 
import sys
import pycurl
import re
import StringIO
import os
import dns.resolver


class PingThread(threading.Thread):

    def __init__(self, ip):
        self.loss = 0
        self.avg = 0
        self.domain = ''

    def run(self):
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


class Consumer(threading.Thread): 

    def __init__(self, queue): 
        threading.Thread.__init__(self)
        self._queue = queue 

    def run(self):
        global valid_ip
        global cur_count
        global mutex
        global total_ip
        while True: 
            msg = self._queue.get()
            if isinstance(msg, str) and msg == 'quit':
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((msg, 443))
            if mutex.acquire(1):
                cur_count += 1
                sys.stdout.write('\rprocessing %6.2f' % (cur_count * 100.0 / total_ip) + '%')
                sys.stdout.flush()
                mutex.release()
            if result == 0:
                self.curl(msg)

    def curl(self, ip):
        try:
            b = StringIO.StringIO()
            conn = pycurl.Curl()
            conn.setopt(pycurl.URL, 'https://' + ip)
            conn.setopt(pycurl.SSL_VERIFYHOST, False)
            conn.setopt(pycurl.WRITEFUNCTION, b.write)
            conn.perform()
            pattern = re.compile(r'<A HREF="https*://(.*):443/"')
            match = pattern.findall(b.getvalue())
            if len(match) > 0:
                valid_ip[ip] = match[0]
        except:
            pass


def get_ip_list():
    answers = dns.resolver.query('_netblocks.google.com', 'TXT')
    pattern = re.compile(r'ip4:(.*?)/')
    match = pattern.findall(str(answers[0]))
    ip_list = filter(lambda x : x[2]!='0', [line.split('.') for line in match])
    other_ip = filter(lambda x : x[2]=='0', [line.split('.') for line in match])
    for ip in other_ip:
        ip_list += [ip[:-2]+[str(i)]+['0'] for i in xrange(1,1)]
    return ip_list


def build_worker_pool(queue, size):
    workers = []
    for _ in xrange(size):
        worker = Consumer(queue)
        worker.start()
        workers.append(worker)
    return workers


def producer():
    global total_ip
    queue = Queue.Queue()
    workers = build_worker_pool(queue, 200)
    ip_list = get_ip_list()
    total_ip = len(ip_list) * 254
    for pre in ip_list:
        ip_prev = '.'.join(pre[:-1])
        for ip in ['.'.join([ip_prev, str(x)]) for x in xrange(1,255)]:
            queue.put(ip)
    for worker in workers:
        queue.put('quit')
    for worker in workers:
        worker.join()


if __name__=='__main__':
    subprocess.call('clear', shell=True)
    print '-' * 60
    print 'get valid ip start'
    valid_ip = {}
    total_ip = 0
    cur_count = 0
    mutex = threading.Lock()
    producer()
    print '\nget valid ip end'
    print '-' * 60
    print len(valid_ip)
