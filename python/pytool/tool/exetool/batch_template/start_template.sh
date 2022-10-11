#!/bin/bash
export LD_LIBRARY_PATH=.:TEMPLATE_ROOT_DIR/lib:$LD_LIBRARY_PATH

ulimit -c unlimited

server_path=TEMPLATE_EXE_DIR
server_name=TEMPLATE_NAME

PID=`ps aux | grep -w  $server_name | grep -v grep | awk '{print $2}'`
if [ -n "$PID" ]; then
        echo "-----------------------[ info  ] this ${server_name} server is running, pid is ${PID} "
else
        cd $server_path
        nohup ./$server_name config/config.xml> /dev/null 2>&1 &

        sleep 1

        PID=`ps aux | grep -w  $server_name | grep -v grep | awk '{print $2}'`
        if [ -n "$PID" ]; then
                echo "-----------------------[  OK   ] this ${server_name} server is ok, pid is ${PID} "
        else
                echo "-----------------------[WARNING] this ${server_name} server is not start"
        fi

fi

echo -e "\n"
