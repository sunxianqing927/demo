#!/bin/bash

server_name=TEMPLATE_NAME
PID=`ps aux | grep -w  $server_name | grep -v grep | awk '{print $2}'`
if [ -n "$PID" ]; then
        kill -9 ${PID}
        echo "-----------------------[  OK   ] this ${server_name} server has been killed"
else
        echo "-----------------------[ info  ] this ${server_name} server is not exit"
fi


