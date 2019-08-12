# Upinator
Small python script which notifies me with Pushbullet if one of my traefik routes goes down.

crontab script

`*/2 * * * *  cat /home/user/Upinator/args.txt | xargs python3 /home/user/Upinator/main.py | while IFS= read -r line; do echo "$(date) $line"; done >> /home/user/Upi    nator/log.log 2>&1`
