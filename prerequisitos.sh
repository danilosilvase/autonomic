#!/bin/bash
yum install -y yum-utils device-mapper-persistent-data lvm2 nano git criu
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo yum-config-manager --enable docker-ce-edge
yum install -y --setopt=obsoletes=0 docker-ce-17.03.1.ce-1.el7.centos docker-ce-selinux-17.03.1.ce-1.el7.centos
systemctl restart docker
echo "{\"experimental\": true, \"metrics-addr\": \"0.0.0.0:9323\"}" >> /etc/docker/daemon.json
systemctl restart docker
yum install openssh-server -y
systemctl start sshd
systemctl enable sshd
