from MobileInventoryCLI.error.error import writeError,obj2dict

	
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import os,sys,json,base64
from colored import attr,fg,bg
from datetime import datetime

class SelectList:
	def __str__(self):
		return 'SelectList'
	def __init__(self,engine,tbl,config):
		self.engine=engine
		self.tbl=tbl
		self.config=config

		#self.displayListMenu()
		self.promptForAction()

	def promptForAction(self):
		while True:
			self.displayListMenu()
			action=input("what would you like to do?: ")
			if action.lower() in ["quit","6"]:
				exit("user quit")
			elif action.lower() in ["back","5"]:
				break
			else:
				try:
					value=int(action)
					print(value)
				except Exception as e:
					print(e)
					writeError(e)

	def displayListMenu(self):
		msg="""
		show Lists -> 1
		goto List -> 2
		show deleted Lists -> 3
		delete list -> 4
		back -> 5
		quit -> 6
		"""
		print(msg)
		return msg
