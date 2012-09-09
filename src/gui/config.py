#-*-python-2.7-
# -*- coding: utf-8 -*-
import ConfigParser

configFile = "config.ini"
domain   = ""
username = ""
password = ""
bindport = ""
#speakers = []

def init():
	global domain, username, password, bindport 
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	domain = config.get('Phone','domain')
	username = config.get('Phone','username')
	password = config.get('Phone','password')
	bindport = config.get('Phone','bindport')
def getSpeakers():
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	speakers = []
	count = int(config.get('Speakers','count'))
	for i in range(0,count):
		name = config.get('Speakers','name['+str(i)+']')
		number = config.get('Speakers','exten['+str(i)+']')
		speaker = {'Name':name ,'Number':number}
		speakers.append(speaker)
	return speakers
