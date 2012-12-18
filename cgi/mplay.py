#!/usr/bin/env python
import os
import socket,urllib
try:
	server=os.environ["SERVER_NAME"]
except:
	server="192.168.91.4"
try:
	filename=os.environ["QUERY_STRING"]
except:
	filename="share/mbl/Shared%20Videos/2012.09.21.Resident.Evil.Damnation.2012.Blu-ray.720p.x264.DTS.MySilu/Resident.Evil.Damnation.2012.Blu-ray.720p.x264.DTS.MySilu.mkv"
	filename="Public/Shared%20Videos/%e6%96%ad%e7%ae%ad.Broken.Arrow.1996.BluRay.720P.DTS.2Audio.x264-CHD/Broken.Arrow.1996.BluRay.720P.DTS.2Audio.x264-CHD.mkv"


filename="/DataVolume/shares/"+urllib.unquote(filename)


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',7890))
s.send("S%s\n"%filename)
d=s.recv(1024)
x=eval(d)
length=x[0].strip()
hour,min,sec=x[0].split(":")
if sec[-1]==',': sec=sec[:-1]
alll=int(hour)*3600+int(min)*60+float(sec)
alll=int(alll)
s.close()
url='http://%s/shares/Public/avs/pl/%s.m3u8'% (server,alll)
print "Status: 302 Moved"
print "Location: %s" % url
print "URI: %s" % url
print "Content-type: text/html\r\n\r\n"

