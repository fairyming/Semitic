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
    mv ./log/eve.json ./upload_eve/tmp/$new_file_name
    # curl -F "clientfile=@./upload_eve/tmp/$new_file_name" -H "Accept: application/json" http://$Server_host
    # 成功
    mv ./upload_eve/tmp/$new_file_name ./upload_eve/success/$new_file_name
    exit
done