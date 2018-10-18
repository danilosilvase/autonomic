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
#start = time.time()

##Init Variables

nodes = json.load(open("/autonomic/conf/nodes.json"))
workers_node = nodes["workers"]
workers_node_names = workers_node.keys()


log_file = open("execute.log","w")


print
print
print ("**************************************************************************")
print ("                            START MIGRATION                               ")
print ("**************************************************************************")
print
print


log_file.write("\n\n\n****************************************     START PLACEMENT    ****************************************\n")


while 1:
    time.sleep(.1)
    start = time.time()

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
    print("\n")

    log_file.write("\n\n\n****************************************     START APP        ****************************************\n")

#os.system('docker network create -d overlay --attachable=true autonomic\n')


    print
    print "+++++++++++++++++++++++++++++++++++++++++++++++"
    print "      Connect to node origin and start app     "
    print "+++++++++++++++++++++++++++++++++++++++++++++++"
    print


#log_file.write("\n\n\n****************************************     CONNECT TO ORIGIN        ****************************************\n")

#    host = workers_node[placement]["address"]
#    user = workers_node[placement]["user"]
#    password = workers_node[placement]["password"]


    host = workers_node["Fog-1"]["address"]
    user = workers_node["Fog-1"]["user"]
    password = workers_node["Fog-1"]["password"]

    hostD = workers_node["Edge-1.2"]["address"]
    userD = workers_node["Edge-1.2"]["user"]
    passwordD = workers_node["Edge-1.2"]["password"]


## conexao remota

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect( hostname = host, username = user, password = password)
 
    sshD = paramiko.SSHClient()
    sshD.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshD.connect( hostname = hostD, username = userD, password = passwordD)


## saida do comando


## Registro inicial de tempo - Remover
    startRemove = datetime.now()
  
    stdin, stdout, stderr = ssh.exec_command('docker rm mqttserver\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Remover
    stopRemove = datetime.now()
    print "Remove Time"
    print stopRemove - startRemove
    print("\n")


## Registro inicial de tempo - Deploy
    startDeploy = datetime.now()
    
    stdin, stdout, stderr = ssh.exec_command('docker run -d --net=auto  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")
    
## Regitro Final do tempo - Deploy
    stopDeploy = datetime.now()
    print "Deploy Time"
    print stopDeploy - startDeploy
    print("\n")

    time.sleep( 30 )

## Registro inicial de tempo - Pull Destination
    startDeploy = datetime.now() 

    stdin, stdout, stderr = sshD.exec_command('docker rm mqttserver\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

    stdin, stdout, stderr = sshD.exec_command('docker rmi eclipse-mosquitto\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

    stdin, stdout, stderr = sshD.exec_command('docker pull eclipse-mosquitto\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Pull Destination
    stopDeploy = datetime.now()
    print "Pull Destination Time"
    print stopDeploy - startDeploy
    print("\n")


 ## Registro inicial de tempo - Checkpoint
    startCheck = datetime.now()

    stdin, stdout, stderr = ssh.exec_command('rm -rf /work/checkpoint1\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

    stdin, stdout, stderr = ssh.exec_command('docker checkpoint create --checkpoint-dir=/work mqttserver checkpoint1\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")


## Regitro Final do tempo - Checkpoint
    stopCheck = datetime.now()
    print "Checkpoint Time"
    print stopCheck - startCheck
    print("\n")


#    stdin, stdout, stderr = ssh.exec_command('tar -czf checkpoint1.tar.gz --absolute-names /work/checkpoint1\n')
#    log_file.write(stderr.read()+"\n")
#    log_file.write(stdout.read()+"\n")

#    stdin, stdout, stderr = ssh.exec_command('sshpass -p "123456" scp checkpoint1.tar.gz root@10.0.1.4:/tmp/\n')
#    log_file.write(stderr.read()+"\n")
#    log_file.write(stdout.read()+"\n")  

    stdin, stdout, stderr = ssh.exec_command('sshpass -p "123456" rsync -razpvvvltogW /work/checkpoint1 root@10.0.1.4:/tmp/\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")


## Regitro Final do tempo - SCP
    stopDeploy = datetime.now()
    print "Deploy Time"
    print stopDeploy - startDeploy
    print("\n")


    stdin, stdout, stderr = ssh.exec_command('hostname\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")


## Registro inicial de tempo - Checkpoint
#    startStop = datetime.now()

#    stdin, stdout, stderr = ssh.exec_command('docker stop mqttserver\n')
#    log_file.write(stderr.read()+"\n")
#    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Checkpoint
#    stopStop = datetime.now()
#    print "Stop Time"
#    print stopStop - startStop
#    print("\n")


## Registro inicial de tempo - Deploy
    startDeploy = datetime.now()

    stdin, stdout, stderr = sshD.exec_command('docker create --net=auto  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Deploy
    stopDeploy = datetime.now()
    print "Deploy Time"
    print stopDeploy - startDeploy
    print("\n")


## Registro inicial de tempo - Deploy
    startDeploy = datetime.now()

    stdin, stdout, stderr = sshD.exec_command('docker start --checkpoint-dir=/tmp/ --checkpoint checkpoint1 mqttserver')
    log_file.write(stderr.read()+"\n")
    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Deploy
    stopDeploy = datetime.now()
    print "Deploy Time"
    print stopDeploy - startDeploy
    print("\n")

    
## Registro inicial de tempo - Checkpoint
#    startStop = datetime.now()


#    stdin, stdout, stderr = ssh.exec_command('docker stop mqttserver\n')
#    log_file.write(stderr.read()+"\n")
#    log_file.write(stdout.read()+"\n")

## Regitro Final do tempo - Checkpoint
#    stopStop = datetime.now()
#    print "Stop Time"
#    print stopStop - startStop
#    print("\n")

    ssh.close()
    sshD.close()


    print("Tempo de execucao")
    end = time.time()
    print(end - start)
    print("\n")

    




