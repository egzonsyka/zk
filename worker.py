#!/usr/bin/env python2.7
import time, socket, os, uuid, sys, kazoo, logging, signal, utils
from election import Election
from utils import MASTER_PATH
from utils import TASKS_PATH
from utils import DATA_PATH
from utils import WORKERS_PATH

class Worker:

   def __init__(self,zk):
        self.zk = zk
        #1.choose a random id
	self.uuid = uuid.uuid4()
	self.path = WORKERS_PATH + str(self.uuid)
        #2.create znode
	self.worker_id = zk.create(self.path, ephemeral=True)
	zk.set(self.worker_id, "non")
	print("Worker %s  created!" %(self.worker_id))
	#3.watch znode
	zk.DataWatch(self.path, self.assignment_change)   		 

     # do something upon the change on assignment
    def assignment_change(self, atask, stat):
	if atask and not atask == "non" :
		#4.5. get task id uppon assignment in workers, get task data in data/yyy
		data_path = DATA_PATH + atask
		if self.zk.exists(data_path) :
			data = self.zk.get(data_path)
			#6. execute task with data
			result = utils.task(data)
			task_path = TASKS_PATH + atask
			task_val = atask + "=" + str(result)

if __name__ == '__main__':
    zk = utils.init()    
    worker = Worker(zk)
    while True:
        time.sleep(1)
