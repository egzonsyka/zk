# Cloud Computing Systems 2016 - ZooKeeper

## General feedback

Just like in first mini-project, you rocked again with the idea! Great! We really enjoyed working on this project. Eventhough we had a lot of other projcets and deadlines, we really had fun with this.
Because almost everything was new to us, starting from Python, Kazoo, Zookeeper, etc., we have learnt a lot which actually is the purpose of our studies. We had difficulties during implementations but we tried to do our best and hopefully we are delivering something that meets your requirements.
ZooKeeper is a great software with clean and simple API. Thanks to the quality of documentation, examples and recipes we could write a distributed software.

## Implementation feedback

Below you can find implementation 

### 2 Leader Election

We completed the leader election class in election.py. We have followed carefuly the recipe in pseudo-code in [Leader Election](http://zookeeper.apache.org/doc/trunk/recipes.html#sc_leaderElection) section in ZooKeeper API documentation.
A simple way of doing leader election with ZooKeeper is to use the SEQUENCE|EPHEMERAL flags when creating znodes that represent "proposals" of clients. 

- Using Kazoo library to implement CRUD operations and set watchers we were able to do our code implementation in *Election* class. 
- We have run three instances of *Election* class and we were able to see that one of them was elected as leader.
- // @Syka to do some filozofejshen here about sending SIGTERM to running instances of election.py


### 3 Master/Worker Architecture

Here we tried to implement the master/worker architecture as you described in [Master/Worker Architecture](https://github.com/ljakupi/zk#3---masterworker-architecture) section.


#### 3.1 Master/Worker components
// @Syka to give some words here, some general words about this section

- We have completed the code in *client.py* in order to make the client able to submit tasks. 
- We have completed the code in *worker.py* in order to amke the worker able to retrieve a task and execute it by calling *utils.py*.
- We finally were able to complete the *master.py*. Here we bind workeres with tasks. *Master* class is responsible to assign tasks to the workers, then the workers process their tasks.

#### 3.2 Fault-Tolerance
// Desc to go here


#### 3.3 ZooKeeper in Cluster Mode
// Desc to go here
