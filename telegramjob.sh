#!/usr/bin/bash

foldername="/home/nick/dev/telegramjob"
cd $foldername
source ./.venv/bin/activate
# /home/nick/dev/telegramjob/.venv/bin/python3 /home/nick/dev/telegramjob/telegramjob.py | tee /home/nick/dev/telegramjob/cron.log 2>&1
# while true; do
python3 ./telegramjob.py | tee ./cron.log 2>&1
#     sleep 900 # wait for 10 minutes
# done

exit 0
