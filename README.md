# YouTube-live-Unifi-Camera
Stream your unifi camera to YouTube live

Run this python script every 5mn in your cronjob

crontab -e

*/5 * * * * /usr/bin/python /root/livecam-caporosso.py >> /var/log/livecam-report.log 2>&1
