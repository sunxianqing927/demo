#!/bin/bash

server_name=TEMPLATE_NAME

PID=`ps aux | grep -w $server_name | grep -v grep | awk '{print $2}'`
    
if [ -n "$PID" ]; then
	echo "-----------------------[  OK   ] this ${server_name} server is ok, pid is ${PID} "
else
	echo "-----------------------[WARNING] this ${server_name} server is not start"
fi
