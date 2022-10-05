#!/bin/bash

mysql_is_installed=$(sudo dpkg -l | grep mysql)
python_is_installed=$(sudo dpkg -l | grep python)
pip_is_installed=$(sudo dpkg -l | grep pip)

if [[ -z $mysql_is_installed ]]
then
	echo y | sudo apt install mysql-server 
fi

if [[ -z $python_is_installed ]]
then
	echo y | sudo apt install python3
fi

if [[ -z $pip_is_installed ]]
then
	echo y | sudo apt install pip3
fi
