#-*-python-2.7-
# -*- coding: utf-8 -*-
class Speaker(object):
	""" Speaker"""
	def __init__(self, name,number):
		super(Speaker, self).__init__()
		self.name = name
		self.number = number