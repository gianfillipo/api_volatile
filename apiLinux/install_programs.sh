#!/bin/bash

mysql=$(sudo dpkg -l | grep mysql)
python=$(sudo dpkg -l | grep python)
pip=$(sudo dpkg -l | grep pip)

if [[ -z $mysql ]]
then
	echo y | sudo apt install mysql-server 
fi

if [[ -z $python ]]
then
	echo y | sudo apt install python3
fi

if [[ -z $pip ]]
then
	echo y | sudo apt install pip3
fi