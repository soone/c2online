#!/bin/bash
if [ $1 == "start" ]; then
	sudo pptpsetup --create testname --server 58.68.151.242 --username chenzm --password chenzm2011 --encrypt --start
	sudo route add -net 192.168.10.0 netmask 255.255.255.0 dev ppp0
fi

if [ $1 == 'stop' ]; then
	sudo route del -net 192.168.10.0 netmask 255.255.255.0
	sudo pidof pptp | sudo xargs kill
fi 
