#!/bin/bash
#Unset NewUser for subsequent attacks
unset NewUser
#Set username and Port
NewUser=`echo $RANDOM`
echo "${NewUser}" > /etc/scripts/NewUser
#LI:
#Add new user
useradd ${NewUser}
#Create password for New user (for brute force attempt)
echo "YourPassword" | passwd --stdin ${NewUser}
#Run Next Attack with sleep
sleep 5
/etc/scripts/NewPort.sh
#Sleep
sleep 5
#Run Next Attack
/etc/scripts/WRSCurl.sh
#Sleep and HB
sleep 10
/opt/ds_agent/dsa_control -m
