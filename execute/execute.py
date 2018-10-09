import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread


startTime = datetime.now()

##Init Variables

nodes = json.load(open("/autonomic/conf/nodes.json"))
workers_node = nodes["workers"]
workers_node_names = workers_node.keys()



log_file = open("execute_log","w")

#log_file.write(startTime)

print
print
print ("**************************************************************************")
print ("                            START MIGRATION                               ")
print ("**************************************************************************")
print
print

log_file.write("\n\n\n****************************************     START MIGRATION	  ****************************************\n")

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Create overlay network                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


log_file.write("\n\n\n****************************************     CREATE OVERLAY        ****************************************\n")

#os.system('docker network create -d overlay --attachable=true autonomic\n')


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Connect to node origin              "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print





#docker run -ti --restart always --name centos --net=rede centos bash

log_file.write("\n\n\n****************************************     CONNECT TO ORIGIN        ****************************************\n")

host = workers_node[workers_node_names[4]]["node"]
user = workers_node[workers_node_names[4]]["user"]
password = workers_node[workers_node_names[3]]["password"]

## conexao remota

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = host, username = user, password = password)

## saida do comando

#stdin, stdout, stderr = ssh.exec_command('docker run -d --net=rede  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
#log_file.write(stderr.read()+"\n")
#log_file.write(stdout.read()+"\n")

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


print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Connect to node destination         "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

log_file.write("\n\n\n****************************************     CONNECT TO DESTINATION       ****************************************\n")

host = workers_node[workers_node_names[3]]["node"]
user = workers_node[workers_node_names[3]]["user"]
password = workers_node[workers_node_names[2]]["password"]


## conexao remota

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname = host, username = user, password = password)

## saida do comando

stdin, stdout, stderr = ssh.exec_command('docker start mqttserver\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

#stdin, stdout, stderr = ssh.exec_command('docker run -d --net=rede  --name mqttserver --security-opt seccomp:unconfined eclipse-mosquitto\n')
#log_file.write(stderr.read()+"\n")
#log_file.write(stdout.read()+"\n")

time.sleep( 60 )

stdin, stdout, stderr = ssh.exec_command('docker stop mqttserver\n')
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

ssh.close()

#stopTime = datetime.now()

#log_file.write(stopTime)
