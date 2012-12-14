#-*-python-2.7-
# -*- coding: utf-8 -*-
import ConfigParser
import md5
import os

HOME = os.getenv("HOME")
configDir = os.path.join(HOME, '.aria')
configFile = os.path.join(configDir, 'config.ini')
#configFile = "config.ini"
domain   = ""
username = ""
password = ""
bindport = ""
passwordhash = None

def init():
	global domain, username, password, bindport
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	domain = config.get('Phone','domain')
	username = config.get('Phone','username')
	password = config.get('Phone','password')
	bindport = config.get('Phone','bindport')
	return config
	
def getSpeakers():
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	speakers = []
	count = int(config.get('Speakers','count'))
	for i in range(count):
		name = config.get('Speakers','name['+str(i)+']')
		number = config.get('Speakers','exten['+str(i)+']')
		speaker = {'Name':name ,'Number':number}
		speakers.append(speaker)
	return speakers

def auth(password):
	global passwordhash
	if passwordhash == None:
		config = ConfigParser.ConfigParser()
		config.read(configFile)
		passwordhash = config.get('General','password')
	hash = md5.new(password)
	if passwordhash == hash.hexdigest():
		return True
	return False

def createConfig():
	config = ConfigParser.RawConfigParser()
	
	config.add_section('General')
	pashash = md5.new()
	password = getUserInput("Password")
	pashash.update(password)
	password = pashash.hexdigest()
	config.set('General', 'password',password)

	config.add_section('Phone')
	domain = getUserInput('Domain','127.0.0.1:5060')
	
	username = getUserInput('username',NotNull=True)
	password = getUserInput('password')
	bindport = getUserInput('bindport','5080')

	config.set('Phone', 'domain',domain)
	config.set('Phone', 'username', username)
	config.set('Phone', 'password' ,password)
	config.set('Phone', 'bindport' ,bindport)

	config.add_section('Speakers')
	count = int(getUserInput('No of Speakers','0'))
	config.set('Speakers', 'count',count)

	for i in range(count):
		print ("For Speaker ("+str(i) +")")
		name = getUserInput('Name',NotNull=True)
		number = getUserInput('Exten No',NotNull=True)
		config.set('Speakers','name['+str(i)+']', name)
		config.set('Speakers','exten['+str(i)+']', number)

	saveConfig(config)

def saveConfig(config):
	# Writing our configuration file to 'example.cfg'
	try:
		os.makedirs(configDir)
	except OSError:
		pass
	with open(configFile, 'wb') as outfile:
		config.write(outfile)


def getUserInput(msg,defaultvalue="",NotNull=False):
	if NotNull:
		defaultvalue ="Not Null"

	while True:
		userInput= str(raw_input(str(msg) + "[" + str(defaultvalue) + "]:"))
		if(len(userInput) == 0):
			if NotNull:
				pass
			else:
				return defaultvalue
		else:
			return userInput

def setPhoneSettings(domain,username,password="",bindport="5080"):
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	try:
		config.add_section('Phone')
	except ConfigParser.DuplicateSectionError, e:
		pass
	finally:
		config.set('Phone', 'domain',domain)
		config.set('Phone', 'username', username)
		config.set('Phone', 'password' ,password)
		config.set('Phone', 'bindport' ,bindport)
		saveConfig(config)

def setPassword(password):
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	try:
		config.add_section('General')
	except ConfigParser.DuplicateSectionError, e:
		pass	
	pashash = md5.new()
	pashash.update(password)
	config.set('General', 'password',pashash.hexdigest())
	saveConfig(config)

def setSpeakers(speakers):
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	try:
		config.add_section('Speakers')
	except ConfigParser.DuplicateSectionError, e:
		pass
	count = len(speakers)
	config.set('Speakers', 'count',count)
	index = 0
	for speaker in speakers:
		name = speaker['Name']
		number = speaker['Number']
		config.set('Speakers','name['+str(index)+']', name)
		config.set('Speakers','exten['+str(index)+']', number)
		index = index + 1
	saveConfig(config)

def isBasicConfigOk():
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	try:
		config.get('General', 'password') 
		config.get('Phone', 'domain')
		config.get('Phone', 'username')
		config.get('Phone', 'password')
		config.get('Phone', 'bindport')
		config.get('Speakers', 'count')
		return True
	except ConfigParser.NoSectionError:
		return False
def isPassWordOk():
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	try:
		config.get('General', 'password')
		return True
	except ConfigParser.NoSectionError:
		return False