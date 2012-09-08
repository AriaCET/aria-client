#-*-python-2.7-
# -*- coding: utf-8 -*-
import ConfigParser
from speaker import Speaker

configFile = "config.ini"
domain   = ""
username = ""
password = ""
bindport = ""
speakers = []

def init():
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	domain = config.get('Phone','domain')
	username = config.get('Phone','username')
	password = config.get('Phone','password')
	bindport = config.get('Phone','bindport')
	count = int(config.get('Speakers','count'))
	for i in range(0,count):
		name = config.get('Speakers','name['+str(i)+']')
		number = config.get('Speakers','exten['+str(i)+']')
		speaker = Speaker(name,number)
		speakers.appends(speaker)

if __name__ == '__main__':
	init()