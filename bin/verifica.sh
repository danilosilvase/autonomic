#!/bin/bash

#name=

#matchingStarted=$(docker ps --filter="name=$name" -q | xargs)
#[[ -n $matchingStarted ]] && docker stop $matchingStarted

#matching=$(docker ps -a --filter="name=$name" -q | xargs)
#[[ -n $matching ]] && docker rm $matching

for container_id in $(docker ps  --filter="name=$name" -q);do docker stop $container_id && docker rm $container_id;done
for container_id in $(docker ps  --filter="name=$name" -q);do docker stop $container_id && docker rm $container_id;done
