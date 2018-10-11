#!/bin/bash
cont=0
while :
do
   python  /autonomic/execute/placement.py
   sleep 60
   let cont=cont+1;
done


