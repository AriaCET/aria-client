# -*- coding: utf-8 -*-
#-*-python-2.7-

__password__ = "test"

def isvalid(password = None):
	if __password__ == password:
		return True
	return False