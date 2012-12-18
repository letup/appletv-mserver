#!/usr/bin/env python

import os,socket
from SocketServer import ThreadingTCPServer
ThreadingTCPServer.allow_reuse_address=True
import threading
import time
import subprocess
clock=threading.Lock()
segbreak="-------SEGMENT-BREAK-------"

currento=None


PATH="/DataVolume/shares/Public/avs/"
class trans:
	def __init__(self,fname,segoff):
		#self.cmd="""/opt/avs/bin/avconv --segment-length 4 --segment-offset %d -threads 4 -ss %d.0 -i "%s" -map 0:0,0:0 -map 0:1,0:1 -vf "crop=1280:720:0:0, scale=1280:720,copy" -aspect 1280:720 -y -f mpegts -async -1 -vcodec libx264 -vcodec copy -bsf:v h264_mp4toannexb -acodec libmp3lame -ab 256k -ar 48000 -ac 2 -""" % (segoff,segoff*4,fname)
		self.filename=fname
		if segoff==0:
			self.cmd=['/opt/avs/bin/avconv','--segment-length','4','--segment-offset','%d'%segoff, '-threads', '4', '-ss', '0.0', '-i', fname, '-map', '0:0,0:0','-map', '0:1,0:1', '-y', '-f', 'mpegts', '-async', '-1', '-vcodec', 'copy', '-bsf:v', 'h264_mp4toannexb', '-acodec', 'libmp3lame', '-ab', '256k', '-ar', '48000', '-ac', '2', '-']
		elif segoff<6:
			self.cmd=['/opt/avs/bin/avconv','--segment-length','4','--segment-offset','%d'%segoff, '-threads', '4', '-ss', '0.0', '-i', fname, '-ss', '%d.0'%(segoff*4), '-map', '0:0,0:0','-map', '0:1,0:1', '-y', '-f', 'mpegts', '-async', '-1', '-vcodec', 'copy', '-bsf:v', 'h264_mp4toannexb', '-acodec', 'libmp3lame', '-ab', '256k', '-ar', '48000', '-ac', '2', '-']
		else:
			self.cmd=['/opt/avs/bin/avconv','--segment-length','4','--segment-offset','%d'%segoff, '-threads', '4', '-ss', '%d.0'%(segoff*4-24), '-i', fname, '-ss', '24.0', '-map', '0:0,0:0','-map', '0:1,0:1', '-y', '-f', 'mpegts', '-async', '-1', '-vcodec', 'copy', '-bsf:v', 'h264_mp4toannexb', '-acodec', 'libmp3lame', '-ab', '256k', '-ar', '48000', '-ac', '2', '-']
		self.segoff=segoff
		self.execseg=-1
		self.readseg=segoff
		self.stop=0
		self.wstop=0
	def finishseg(self):
		self.fts.close()
		clock.acquire()
		self.execseg=self.segcount
		clock.release()
		if self.segcount>=15:
			try:
				os.unlink(PATH+"segment_%d.ts" % (self.segcount-15))
			except:
				pass
		while 1:
			clock.acquire()
			myseg=self.readseg
			self.wstop=self.stop
			clock.release()
			if self.wstop==1:
				return
			if self.segcount>myseg+10:
				time.sleep(1)
			else:
				break
			
		self.segcount+=1
		self.fts=file(PATH+"segment_%d.ts" % self.segcount,"w")
	def start(self):
		f=subprocess.Popen(self.cmd,stdout=subprocess.PIPE)
		self.segcount=self.segoff
		self.fts=file(PATH+"segment_%d.ts" % self.segcount,"w")
		lret=""
		while 1:
			ret=f.stdout.read(1048576)
			if len(ret)==0:
				if len(lret)>0:
					self.fts.write(lret)
				self.fts.close()
				break
			if len(lret)>0:
				nret=lret+ret
				fo=0
				while 1:
					pos=nret.find(segbreak)
					if pos>=0:
						fo=1
						self.fts.write(nret[:pos])
						self.finishseg()
						if self.wstop==1:
							os.kill(f.pid,15)
							return
						nret=nret[pos+len(segbreak):]
					else:
						break
				if fo==1:
					lret=nret
				else:
					self.fts.write(lret)
					self.fts.write(ret[:-1*len(segbreak)])
					lret=ret[-1*len(segbreak):]
			else:
				while 1:
					pos=ret.find(segbreak)
					if pos>=0:
						self.fts.write(ret[:pos])
						self.finishseg()
						if self.wstop==1:
							os.kill(f.pid,15)
							return
						ret=ret[pos+len(segbreak):]
					else:
						break
				self.fts.write(ret[:-1*len(segbreak)])
				lret=ret[-1*len(segbreak):]

def info(fn):
	cmd="""/opt/avs/bin/avprobe "%s" 2>&1"""  % fn
	f=os.popen(cmd)
	data=f.read()
	f.close()
	lines=data.split("\n")
	length=''
	video=''
	audio=[]
	for line in lines:
		fields=line.split()
		if len(fields)<3:continue
		if fields[0]=='Duration:':
			length=fields[1]
		elif fields[0]=='Stream':
			if fields[2]=='Video:':
				video=fields[1]
			elif fields[2]=='Audio:':
				audio.append(fields[1])
	return length,video,audio

class Handler:
	def __init__(self,request,client_address,server):
		rfile = request.makefile('rb',-1)
		wfile = request.makefile('wb', 0)
		data=''
		while 1:
			word=rfile.read(1)
			if word=='\n':
				break
			data=data+word
		ret=self.parse(data.strip())
		wfile.write(ret);
		if not wfile.closed:
			wfile.flush()
		wfile.close()
		rfile.close()
		request.shutdown(socket.SHUT_RDWR)
	def parse(self,data):
		global currento
		if data[0]=='S':
			fn=data[1:]
			ret=str(info(fn))
			if currento is not None:
				clock.acquire()
				currento.stop=1
				clock.release()
			currento=trans(fn,0)
			t=threading.Thread(target = currento.start,args=())
			t.setDaemon(1)
			t.start()
		elif data[0]=='G':
			seg=int(data[1:])
			if currento is None:
				return "ERROR"
			clock.acquire()
			ex=currento.execseg
			clock.release()
			if seg>=ex-15 and seg<=ex:
				ret=PATH+"segmeng_%d.ts"%seg
				clock.acquire()
				currento.readseg=seg
				clock.release()
			elif seg>ex and seg<ex+10:
				while 1:
					time.sleep(1)
					clock.acquire()
					ex=currento.execseg
					currento.readseg=seg
					clock.release()
					if ex>=seg:
						ret=PATH+"segmeng_%d.ts"%seg
						break
			else:
				fn=currento.filename
				clock.acquire()
				currento.stop=1
				clock.release()
				currento=trans(fn,seg)
				t=threading.Thread(target = currento.start,args=())
				t.setDaemon(1)
				t.start()
				while 1:
					time.sleep(1)
					clock.acquire()
					ex=currento.execseg
					clock.release()
					if ex>=seg:
						ret=PATH+"segmeng_%d.ts"%seg
						break
		else:
			ret='ERROR'
		return ret


server=ThreadingTCPServer(('0.0.0.0',7890),Handler)
		


server.serve_forever()

