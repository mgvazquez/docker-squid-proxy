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

squid_cache = "squid -z"
squid_run = "squid -N"

iptables_add_redirect = "iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to " + squid_listen_port + " -w"
iptables_rm_redirect = iptables_add_redirect.replace(' -A ', ' -D ')



class SquidContext:
    def __enter__(self):
        print("Starting Squid")
        try:
            # subprocess.check_call(iptables_add_redirect.split())
            self.squid_process = subprocess.Popen(squid_run, shell=True)
            self.setup = True
        except:
            print("Starting Squid: FAIL")
            self.setup = False
        return self

    def __exit__(self, type, value, traceback):
        if self.setup:
            print("Stopping Squid")
            self.squid_process.kill
            # subprocess.check_call(iptables_rm_redirect.split())

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
        # Wait for the squid instance to end or a ctrl-c
        # signal.signal(signal.SIGTERM, graceful_shutdown)
        try:
            while True:
                time.sleep(1)
            # while is_port_open(int(squid_listen_port)) and status["shutting_down"] is False:
            #     time.sleep(1)
        except KeyboardInterrupt as ex:
            # Catch Ctrl-C and pass it into the squid instance
            print("CTRL-C caught, shutting down.")
        except Exception as ex:
            print("Caught exception, %s, shutting down" % ex)












    # while not is_port_open(int(squid_listen_port)):
    #     print("Waiting for Squid port (%s/tcp) to open..." % squid_listen_port)
    #     time.sleep(1)








    # if is_port_open(squid_listen_port):
    #
    #
    #
    #
    #
    #
    # else:
    #     print("Port %s never opened, squid instance"
    #           " must have terminated prematurely" % squid_listen_port)
    # return 0




    # subprocess.check_call(squid_cache, shell=True)
    #
    # time.sleep(2)
    #
    #
    # squid_p = subprocess.Popen(squid_run, shell=True)
    # print squid_p.__dict__
    # print squid_p.poll()
    #
    # while squid_p.poll() is None:
    #     signal.signal(signal.SIGTERM, graceful_shutdown)
    #     time.sleep(1)



    # with RedirectContext():
    #     # Wait for the squid instance to end or a ctrl-c
    #     signal.signal(signal.SIGTERM, graceful_shutdown)
    #     try:
    #         while is_port_open(int(squid_listen_port)) and status["shutting_down"] is False:
    #             time.sleep(1)
    #     except KeyboardInterrupt as ex:
    #         # Catch Ctrl-C and pass it into the squid instance
    #         print("CTRL-C caught, shutting down.")
    #     except Exception as ex:
    #         print("Caught exception, %s, shutting down" % ex)



if __name__ == '__main__':
    sys.exit(main())
