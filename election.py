#!/usr/bin/env python2.7
import time, socket, os, uuid, sys, kazoo, logging, signal, inspect
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import KazooException

class Election:

   def __init__(self, zk, election_path, self_path):
        self.election_path = election_path
        self.zk = zk
	self.is_leader = False
	self.child_id = self_path.split("/")[2]
	self.path = self_path
	self.leader_path = None
    
		 
    def is_leading(self):
		#TO COMPLETE
		
	#perform a vote..	
    def ballot(self,children):
	next_master = min(children)
	master_path = self.election_path + "master_current/"
	self.zk.ensure_path(master_path)
	self.leader_path = master_path + next_master
	if(self.child_id == next_master) :
		self.zk.create(self.leader_path, ephemeral=True) 
		print("I'm the leader now")
		self.is_leader = True
		return True
	else:
		print ("Master is = %s " %(self.leader_path)) 
		self.zk.exists(self.leader_path, self.on_node_delete) 
		self.is_leader = False
		return False

                    
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
