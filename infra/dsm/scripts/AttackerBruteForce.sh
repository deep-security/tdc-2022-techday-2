#!/bin/bash
#Install expect - already installed via infra script
#yum install -y expect
#Get VictimIP from file
VictimIP=`cat /etc/scripts/VictimIP`
#Create script to bypass key check 
echo '#!/usr/bin/expect -f'	> /etc/scripts/bruteforce.sh
echo "spawn ssh ec2-user@${VictimIP}" >> /etc/scripts/bruteforce.sh
echo 'expect "yes/no) "' >> /etc/scripts/bruteforce.sh
echo 'send "yes\r"' >> /etc/scripts/bruteforce.sh
echo 'expect "assword: "' >> /etc/scripts/bruteforce.sh
echo 'send "WrongPassword\r"' >> /etc/scripts/bruteforce.sh
#Create script to fail login
echo '#!/usr/bin/expect -f'	> /etc/scripts/bruteforce2.sh
echo "spawn ssh ec2-user@${VictimIP}" >> /etc/scripts/bruteforce2.sh
echo 'expect "assword: "' >> /etc/scripts/bruteforce2.sh
echo 'send "WrongPassword\r"' >> /etc/scripts/bruteforce2.sh
echo 'expect "assword: "' >> /etc/scripts/bruteforce2.sh
echo 'send "WrongPassword\r"' >> /etc/scripts/bruteforce2.sh
echo 'expect "assword: "' >> /etc/scripts/bruteforce2.sh
echo 'send "WrongPassword\r"' >> /etc/scripts/bruteforce2.sh
#Make scripts executable
chmod +x /etc/scripts/bruteforce.sh
chmod +x /etc/scripts/bruteforce2.sh
#Run script that accepts key check 
/etc/scripts/bruteforce.sh
#Run script enough to trigger LI Rule 1002828 - Application - Secure Shell Daemon (SSHD)
for i in {1..15}; do /etc/scripts/bruteforce2.sh & done
#echo GO publish SNS topic
echo "GO"