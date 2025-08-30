#!/usr/bin/bash

cd "$(dirname "$0")"

if [ "$1" == "--install-cron" ]; then
    echo "Installing cron job..."
    (crontab -l 2>/dev/null; echo "*/30 9-21 * * * $(realpath $0)") | crontab -
    echo "Cron job installed."
    exit 0
fi

# foldername="/home/nick/dev/telegramjob"
# cd $foldername

# source ./.venv/bin/activate

# /home/nick/dev/telegramjob/.venv/bin/python3 /home/nick/dev/telegramjob/telegramjob.py | tee /home/nick/dev/telegramjob/cron.log 2>&1
# while true; do
#python3 ./telegramjob.py | tee ./cron.log 2>&1
# python3 ./telegramjob.py

uv run ./telegramjob.py
#     sleep 900 # wait for 10 minutes
# done

exit 0