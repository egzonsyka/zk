#!/usr/bin/env python2.7
import time, socket, os, uuid, sys, kazoo, logging, signal, inspect
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import KazooException

class Election:

    def __init__(self, zk, path, func,args):
        self.election_path = path
        self.zk = zk
		self.is_leader = False
        if not (inspect.isfunction(func)) and not(inspect.ismethod(func)):
            logging.debug("not a function "+str(func))
            raise SystemError
		#TO COMPLETE
		 
    def is_leading(self):
		#TO COMPLETE
		
	#perform a vote..	
    def ballot(self,children):
		#TO COMPLETE
                    
if __name__ == '__main__':
    zkhost = "127.0.0.1:2181" #default ZK host
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
    if len(sys.argv) == 2:
        zkhost=sys.argv[2]
        print("Using ZK at %s"%(zkhost))
   
	#TO COMPLETE
    #ADD misisng initialization... 
   
    while True:
        time.sleep(1)
