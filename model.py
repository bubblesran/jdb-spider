#-*-coding: utf-8-*-

from peewee import *
import datetime

database = SqliteDatabase('jobsdb.db')

class BaseModel(Model):
	class Meta:
		database = database

class quickinfo(BaseModel):
	id 		= PrimaryKeyField()
	title 		= CharField()
	link 		= CharField(unique=True)
	summary 	= CharField()
	salary 	= CharField()
	postdate 	= CharField()
	updatetime  = DateTimeField(default=datetime.datetime.now)

class detailinfo(BaseModel):
	ref_jobsdb = PrimaryKeyField()
	title 		= CharField()
	link 		= CharField(unique=True)
	datePosted 	= CharField()
	Responsibilities 		= CharField()
	Requirements 	= CharField()
	CareerLevel 		= CharField()
	Exp 	= CharField()
	Qualification 		= CharField()
	salary 	= CharField()

def database_init():
    database.connect()
    database.create_tables([quickinfo, detailinfo], safe=True)
    database.close()
