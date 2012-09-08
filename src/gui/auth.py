# -*- coding: utf-8 -*-

__authentication__ = False
__password__ = "test"

def isvalid(ipstr = None):
	global __authentication__
	if not __authentication__ and __password__ == ipstr:
		__authentication__ = True
	return __authentication__

def reset():
	__authentication__ = False	