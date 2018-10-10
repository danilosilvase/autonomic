#!/bin/env python
#coding: utf8

import os
import paramiko
import random
import time
import json
import sys
import operator
from datetime import datetime
from threading import Thread
from random import choice

#current_time=$(date "+%Y.%m.%d-%H.%M.%S")

#file_name=test_files.log


startTime = datetime.now()

##Init Variables

nodes = json.load(open("/autonomic/conf/nodes.json"))
workers_node = nodes["workers"]
workers_node_names = workers_node.keys()


log_file = open("execute.log","w")


print
print
print ("**************************************************************************")
print ("                            START PLACEMENT                               ")
print ("**************************************************************************")
print
print




log_file.write("\n\n\n****************************************     START PLACEMENT    ****************************************\n")

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "                Choice Fog node                "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


placement=choice(workers_node_names)

print(placement)


log_file.write("\n\n\n****************************************     START APP        ****************************************\n")

#os.system('docker network create -d overlay --attachable=true autonomic\n')


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Connect to node origin and start app     "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

#docker run -ti --restart always --name centos --net=rede centos bash

#log_file.write("\n\n\n****************************************     CONNECT TO ORIGIN        ****************************************\n")

host = workers_node[placement]["address"]
user = workers_node[placement]["user"]
password = workers_node[placement]["password"]

## conexao remota

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = host, username = user, password = password)

## saida do comando

stdin, stdout, stderr = ssh.exec_command('docker run -d --net=rede  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

stdin, stdout, stderr = ssh.exec_command('docker start mqttserver\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

stdin, stdout, stderr = ssh.exec_command('hostname\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

time.sleep( 60 )

stdin, stdout, stderr = ssh.exec_command('docker stop mqttserver\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

ssh.close()




