#!/bin/bash
if [ ! -f ./conf/Semitic.conf ]; then
    echo `date '+%Y-%m-%d %H:%M:%S'` "config file not exist"
    echo `date '+%Y-%m-%d %H:%M:%S'` "config file not exist" > ./log/Semitic.log
    exit 0
fi
. ./conf/Semitic.conf

while true
do
    new_file_name="eve_`date '+%Y%m%d%H%M%S'`.json"
    cp ./log/eve.json ./upload_eve/$new_file_name
    cat /dev/null > ./log/eve.json
    curl -F "clientfile=@./upload_eve/$new_file_name" -H "Accept: application/json" http://$Server_host/api/upload_eve

    #if [ $? -eq 0 ]; then
       # mv ./upload_eve/tmp/$new_file_name ./upload_eve/success/$new_file_name
    #else
        #mv ./upload_eve/tmp/$new_file_name ./upload_eve/error/$new_file_name
    #fi
    sleep $heartbeat_time
done