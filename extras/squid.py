#!/usr/bin/env python

import os
import subprocess
import socket
import sys
import time
import signal

squid_listen_port = os.getenv("SQUID_LISTEN_PORT", '3128')
squid_max_cache_size = os.getenv("SQUID_MAX_CACHE_SIZE", '5000')
squid_max_cache_object = os.getenv("SQUID_MAX_CACHE_OBJECT", '1024')

squid_cache = 'squid -z'
squid_run = 'squid -N'
squid_stop = 'squid -k shutdown'

iptables_add_redirect = "iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to " + squid_listen_port + " -w"
iptables_rm_redirect = iptables_add_redirect.replace(' -A ', ' -D ')

class SquidContext:
    def __enter__(self):
        try:
            print("Starting Squid")
            self.squid_cache_proc = subprocess.check_call(squid_cache, shell=True)
            self.squid_proc = subprocess.Popen(squid_run, shell=True)
            self.iptables_add_proc = subprocess.check_call(iptables_add_redirect.split())
            self.setup = True
        except:
            print("Starting Squid: FAIL")
            self.setup = False
        return self

    def __exit__(self, type, value, traceback):
        if self.setup:
            print("Stopping Squid")
            print self.iptables_add_proc
            if self.iptables_add_proc == 0:
                subprocess.check_call(iptables_rm_redirect.split())
            subprocess.check_call(squid_stop, shell=True)
            time.sleep(1)

def is_port_open(port_num):
    """ Detect if a port is open on localhost"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(('127.0.0.1', port_num)) == 0

def main():
    if os.path.exists("/var/cache/squid/squid.pid"):
        os.remove("/var/cache/squid/squid.pid")

    squid_initial_conf = []
    squid_initial_conf.append('http_port %s intercept' % squid_listen_port)
    squid_initial_conf.append('maximum_object_size %s MB' % squid_max_cache_object)
    squid_initial_conf.append('cache_dir ufs /var/cache/squid %s 16 256' % squid_max_cache_size)

    with open("/etc/squid/squid.d/00-initial.conf", 'w') as conf_file:
        for conf in squid_initial_conf:
            print("Appending to /etc/squid/squid.d/00-initial.conf: [%s]" % conf)
            conf_file.write(conf + '\n')

    status = {'shutting_down': False}

    def graceful_shutdown(signal, frame):
        """Clean shutdown"""
        print("SIGTERM caught, shutting down.")
        status["shutting_down"] = True

    with SquidContext() as squid:
        signal.signal(signal.SIGTERM, graceful_shutdown)
        try:
            time.sleep(5)
            while is_port_open(int(squid_listen_port)) and status["shutting_down"] is False:
                time.sleep(1)
        except KeyboardInterrupt as ex:
            print("CTRL-C caught, shutting down.")
        except Exception as ex:
            print("Caught exception, %s, shutting down" % ex)

if __name__ == '__main__':
    sys.exit(main())
