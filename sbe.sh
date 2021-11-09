#!/bin/bash


RED="\e[1;31m"
REDEND="\e[0m"

echo -e "\e[1;32m
			        #     #  #####  #######
 			#    #  ##    # #     # #
  			  # #   # #   # #       #
			### ### #  #  #  #####  #####
  			  # #   #   # #       # #
 			#    #  #    ## #     # #
        			#     #  #####  #######
\e[0m"
echo -e "\e[1;32m	  Simple Enumeration Script\e[0m"
echo -e "\e[1;32mBeginning Enumeration.....\e[0m\n\n\n"

echo -e "${RED}Whoami:${REDEND}\n"
whoami

echo -e "\n\n${RED}ID:${REDEND}\n"
id

echo -e "\n\n${RED}uname -a:${REDEND}\n"
uname -a

echo -e "\n\n${RED}Hostname:${REDEND}\n"
hostname

echo -e "\n\n${RED}etc/passwd output:${REDEND}\n"
cat /etc/passwd

echo -e "\n\n${RED}etc/issue output:${REDEND}\n"
cat /etc/issue

echo -e "\n\n${RED}etc/*-release output:${REDEND}\n"
cat /etc/*-release

echo -e "\n\n${RED}IP Address:${REDEND}\n"
ip a
echo -e "\n\n${RED}Host Routes:${REDEND}\n"
/sbin/route

echo -e "\n\n${RED}Cronjobs:${REDEND}\n"
ls -lah /etc/cron.*

echo -e "\n\n${RED}Crontab:${REDEND}\n"
cat /etc/crontab

echo -e "\n\n${RED}Writeable Directories:${REDEND}\n"
find / -writable -type d 2>/dev/null

echo -e "\n\n${RED}Mounted Disks:${REDEND}\n"
cat /etc/fstab

echo -e "\n\n${RED}All Available Disks:${REDEND}\n"
lsblk

echo -e "\n\n${RED}SUID Files:${REDEND}\n"
find / -perm -u=s -type f 2>/dev/null

echo -e "\n\n${RED}Network Connections:${REDEND}\n"
netstat -antup


echo -e "\n\n${RED}Files with Capabilities:${REDEND}\n"
getcap -r / 2>/dev/null

