#!/bin/bash
if [ ! -f ./conf/Semitic.conf ]; then
    echo `date '+%Y-%m-%d %H:%M:%S'` "config file not exist"
    echo `date '+%Y-%m-%d %H:%M:%S'` "config file not exist" > ./log/Semitic.log
    exit 0
fi
. ./conf/Semitic.conf

cmd="suricata -i $Netcard -c ./conf/suricata.yaml -S ./rules/local.rules -l log"
nohup $cmd > ./log/Semitic.log &