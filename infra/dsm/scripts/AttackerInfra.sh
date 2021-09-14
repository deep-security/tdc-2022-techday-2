#!/bin/bash
#### LI Attack Infra
yum install -y expect
yum install -y jq
#set password auth
sed -i '/PasswordAuthentication no/s/^/#/g' /etc/ssh/sshd_config
sed -i '/PasswordAuthentication yes/s/^#//g' /etc/ssh/sshd_config
service sshd restart


