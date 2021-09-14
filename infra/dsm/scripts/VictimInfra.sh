#!/bin/bash
####Ill use jq somewhere
yum -y install jq
####IM Attack
yum -y install nmap-ncat
#Enable Password logins
sed -i '/PasswordAuthentication no/s/^/#/g' /etc/ssh/sshd_config
sed -i '/PasswordAuthentication yes/s/^#//g' /etc/ssh/sshd_config
#restart sshd to make ssh access take effect. 
service sshd restart
#File for XDR Threat to "steal"
mkdir /etc/finance
cd /etc/finance
curl https://osce-installer.s3.amazonaws.com/payroll_data.csv --output payroll_data.csv -s
adduser service_payroll
echo service_payroll:payrollService1234 | chpasswd
usermod -aG wheel service_payroll