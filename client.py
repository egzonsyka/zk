#!/usr/bin/env python2.7
import time, socket, os, uuid, sys, kazoo, logging, signal, utils, random
from election import Election
from utils import MASTER_PATH
from utils import TASKS_PATH
from utils import DATA_PATH
from utils import WORKERS_PATH

class Client:

    def __init__(self,zk):
        self.zk = zk	

    def compute_task(self):
	task_id = random.randint(100, 99999)
	task = TASKS_PATH + str(task_id)
	task_path = self.zk.create(task, ephemeral = True)
	task_data = str(task_id)
	#Setting data
	zk.set(task, task_data)
	data = DATA_PATH + str(task_id)
	data_path = self.zk.create(data, ephemeral = True)
	data_value = str(random.randint(1, 100))
	zk.set(data_path, data_value)
	print("New task with id  = %s and data = %s" %(task_data, data_value))
	return task_path

    def submit_task(self):
        new_task_path = self.compute_task()
	watcher = zk.DataWatch(new_task_path, self.task_completed)
  		
    #REACT to changes on the submitted task..				   
    def task_completed(self, data, stat):
	if data and ("," in data) : 
		data_stats =  data.split(",")
		print("Task %s Stats %s" %(data_stats[0], data_stats[1]))
        elif data and ("=" in data):
		data_res = data.split("=", 2)
		task_path = TASKS_PATH + data_res[0]
		data_path = DATA_PATH + data_res[0]
		result = data_res[1]
		print("Task %s executed with result: %s" %(data_res[0], result))
		zk.delete(task_path)
		zk.delete(data_path) 
	
    def submit_task_loop(self):
        while True:
            self.submit_task()
	    time.sleep(30)

if __name__ == '__main__':
    zk = utils.init()    
    client = Client(zk)
    client.submit_task_loop()
    while True:
        time.sleep(1)

