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
    
		 
    def kill_myself(self,signum, frame):
	self.zk.delete(self.path)
	if(self.is_leader) :
		self.zk.delete(self.leader_path)
	kill_now = True	
		 
    def is_leading(self):
	return self.is_leader	
		

    def on_node_delete(self, event) :
	#in case of deletion start elections(perform a vote)
	if event.type == kazoo.protocol.states.EventType.DELETED:
		print 'Master died'
		self.ballot(self.zk.get_children(self.election_path))
		
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

def leader_func():
	print("I am the leader now")

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        logging.info('Session lost')
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        logging.info('Disconnected')        
    else:
        # Handle being connected/reconnected to Zookeeper
        logging.info('Connected')
                    
if __name__ == '__main__':
    zkhost = "127.0.0.1:2181" #default ZK host
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
    if len(sys.argv) == 2:
        zkhost=sys.argv[2]
        print("Using ZK at %s"%(zkhost))
    zk = KazooClient(zkhost) 
    zk.add_listener(my_listener)
    zk.start()
   
    master_path = MASTER_PATH + "guid_"
    child = zk.create(master_path, ephemeral=True, sequence=True)
    election = Election(zk, MASTER_PATH, child)

    if election.ballot(zk.get_children(MASTER_PATH)) == False :
	print("I'm a worker")

    while (kill_now == False) :
        time.sleep(1)
    print("I was killed gracefully")
