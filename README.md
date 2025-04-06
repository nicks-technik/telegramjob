# telegramjob

playwright install

playwright codegen https://www.youtube.com/watch?v=QJL6uV7z-8I


### Generate new token.pickle
    rm token.pickle
    python3 ./youtubestuff.py # generate new and login to Google account


python3 telegramjob.py

telegramjob.sh # calls the python script

### CRON JOB ###
*/30 9-20 * * * cd /home/nick/dev/telegramjob && ./telegramjob.sh
