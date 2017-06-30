#-*-coding: utf-8-*-

from peewee import *
import datetime

database = SqliteDatabase('jobsdb.db')

class BaseModel(Model):
	class Meta:
		database = database # this model uses database jobsdb.db

class quickinfo(BaseModel):
	id         = CharField()
	title      = CharField()
	link       = CharField()
	summary    = CharField()
	salary     = CharField()
	postdate   = CharField()
	updatetime = DateTimeField(default=datetime.datetime.now)

class detailinfo(BaseModel):
	ref              = CharField(primary_key=True)
	title            = CharField()
	link             = CharField()
	datePosted       = CharField()
	Responsibilities = CharField()
	Requirements     = CharField()
	CareerLevel      = CharField()
	Exp              = CharField()
	Qualification    = CharField()
	salary           = CharField()

def database_init():
    database.connect()
    database.create_tables([quickinfo, detailinfo])
    database.close()
