#!/usr/bin/env python
import socket, subprocess, urllib, json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

#DEFINE WAN IP FIX ADDRESS OR DDNS AND PORT
host = 'YOUR_WANIP_OR_DDNS' #<-- CHANGE ME
port = 7447

#DEFINE UNIFI CAMERA ID MANAGED BY YOUR NVR
camID = 'YOUR_UNIFI_CAMERA_ID' #<-- CHANGE ME

#DEFINE YouTube API, Live Key and Channel id
API_KEY = 'YOUR_YOUTUBE_API_KEY' #<-- CHANGE ME
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = "v3"
livekey = 'YOUR_YOUTUBE_LIVE_KEY' #<-- CHANGE ME
channelId = 'YOUR_YOUTUBE_CHANNEL_ID' #<-- CHANGE ME
rtmp = 'rtmp://a.rtmp.youtube.com/live2'

#DEFINE FFMPEG COMMAND
ffmpegcmd = 'ffmpeg -loglevel 16 -re -rtsp_transport tcp -i rtsp://' +str(host)+ ':' +str(port)+'/' +str(camID)+' -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv '+str(rtmp)+'/' + str(livekey)

#REQUEST TO YOUTUBE API TO SEARCH LIVE STATUS
url = 'https://www.googleapis.com/youtube/v3/search?part=id&channelId='+str(channelId)+'&eventType=live&type=video&key='+str(API_KEY)
data = json.load(urllib.urlopen(url))

livestatus = (data['pageInfo']['totalResults'])

if livestatus == 0:
	print 'YouTube Live broadcast is offline'
	try:
		subprocess.Popen('killall -9 ffmpeg', shell=True)
		#CHECK INTERNET CONNECTION AND PORT IF OK EXEC ffmpeg command
		s.connect((host, port))
		s.shutdown(2)
		print 'Connected to NVR'
		print host + " on port: " + str(port)
		subprocess.Popen(ffmpegcmd, shell=True)
	except:
		print 'Cannot connect to NVR for the moment I will retry in 5mn set in cronjob'
else:
	print 'Already on live'
