#!/bin/bash
#Unset NewPort for subsequent attacks
unset NewPort
#Set username and Port
NewUser=`cat /etc/scripts/NewUser`
NewPort=`echo ${RANDOM}`

#IM:
#Enable Password logins
#sed -i '/PasswordAuthentication no/s/^/#/g' /etc/ssh/sshd_config
#sed -i '/PasswordAuthentication yes/s/^#//g' /etc/ssh/sshd_config
#restart sshd to give make ssh access take effect. 
#service sshd restart

#Install netcat (already installed via infrastructure script)
#yum -y install nmap-ncat
#Triggers rule 	1002875 - Unix - Added or Removed Software OPTIONAL ADDITIONAL TASK

#creat script to be ran as backdoor user in new session
echo "nc -l ${NewPort} -4 &" > /home/${NewUser}/openport.sh

#make script executable
chmod +x /home/${NewUser}/openport.sh

#run open port as new user
su ${NewUser} -c /home/${NewUser}/openport.sh
#1003168 - Open Port Monitor - IM rule triggered (port opened as newly created user)
