#!/usr/bin/env python2.7
import time, socket, os, uuid, sys, kazoo, logging, signal, utils
from kazoo.protocol.states import EventType
from election import Election
from utils import MASTER_PATH
from utils import TASKS_PATH
from utils import DATA_PATH
from utils import WORKERS_PATH

class Master:
    #initialize the master
    def __init__(self,zk):
        self.master = False
        self.zk = zk
	my_path = zk.create(MASTER_PATH, ephemeral=True, sequence=True)
	self.election = Election(zk, MASTER_PATH, my_path)
	self.election.ballot(self.zk.get_children(MASTER_PATH))
	zk.ChildrenWatch(WORKERS_PATH,self.assign, send_event=True)
	zk.ChildrenWatch(TASKS_PATH, self.assign, send_event=True)

    def compute_free_worker(self):
	workers = self.zk.get_children(WORKERS_PATH)
	found_worker = False
	if not workers == None : 
		for i in range(0,len(workers)) :
			worker_path = WORKERS_PATH + workers[i]
			val = self.zk.get(worker_path)
			# Check if no task is assigned to the worker
			if ("non" in val) :
				found_worker = True
				return  workers[i]
        return None

    #assign tasks 				   
    def assign(self, children, event):
        if self.election.is_leading():
            if(event) :
       	        print("Change happened with event  = %s" %(event.type))
	    tasks = self.zk.get_children(TASKS_PATH)
	    for i in range(0,len(tasks)) :
                task_path = TASKS_PATH + tasks[i]
	        task_data = self.zk.get(task_path)
	        if("," not in task_data) : # not assigned
		    free_worker = self.compute_free_worker()
		    if not free_worker == None :
                        worker_path = WORKERS_PATH + free_worker
		        print("Assigned worker = %s to task = %s" %(free_worker, tasks[i]))
		        new_task_data = []
		        new_task_data.append(task_data)
		        new_task_data.append(",")
		        new_task_data.append(free_worker)
		        self.zk.set(task_path, str(new_task_data))
		        self.zk.set(worker_path, str(tasks[i]))
		        self.zk.get(worker_path, self.finished_task)
			
    def finished_task(self, data) :
	if data and data == "non" : # Worker completed its task
		self.assign(data)
				
                
if __name__ == '__main__':
    zk = utils.init()
    master = Master(zk)
    while True:
        time.sleep(1)

