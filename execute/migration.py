
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

startTime = datetime.now()
start = time.time()

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
#stop_app = time.time()

while 1:
    time.sleep(.1)


    print
    print "+++++++++++++++++++++++++++++++++++++++++++++++"
    print "                Choice Fog node                "
    print "+++++++++++++++++++++++++++++++++++++++++++++++"
    print

## Registro inicial de tempo - Algoritmo
    startChoice = datetime.now()  
 

## Escolha do no
    placement=choice(workers_node_names)
    print(placement)

## Regitro Final do tempo - Algoritmo
    stopChoice = datetime.now()
    print "Choice Time"
    print stopChoice - startChoice


#    print(datetime.now() - startTime)

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


## Registro inicial de tempo - Deploy
    startDeploy = datetime.now()
    

    stdin, stdout, stderr = ssh.exec_command('docker run -d --net=rede  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")
    

## Regitro Final do tempo - Algoritmo
    stopDeploy = datetime.now()
    print "Deploy Time"
    print stopDeploy - startDeploy


## Registro inicial de tempo - Deploy
    startService = datetime.now()

    stdin, stdout, stderr = ssh.exec_command('docker start mqttserver\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")


## Regitro Final do tempo - Algoritmo
    stopService = datetime.now()
    print "Start Time Service"
    print stopService - startService


    stdin, stdout, stderr = ssh.exec_command('hostname\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

    time.sleep( 120 )
    
    stdin, stdout, stderr = ssh.exec_command('docker stop mqttserver\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

#   print("--- %s seconds ---" % (time.time() - startTime))

    ssh.close()


    print("Tempo de execucao")
    end = time.time()
    print(end - start)

    




