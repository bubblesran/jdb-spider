#-*-coding: utf-8-*-

import core
import model
from model import quickinfo
import datetime
import requests
#import dprocess 
#for daily routine work, the data process is not worked as expected yet. Better do it in another programme.

def get_linklist():
	res = []
	for info in quickinfo.select().where(quickinfo.updatetime>=datetime.datetime.combine(datetime.date.today(), datetime.time.min)):
		res.append((info.link,info.label))
	return res

def ifttt_msg(msg1, msg2):
	report={}
	report['value1'] = msg1
	report['value2'] = msg2
	requests.post("https://maker.ifttt.com/trigger/crawl/with/key/gJ3YX4tfFuB2C-2ZJp4W",data=report)

def main():
	keywords = [u'data+scientist', u'data+analyst', u'business+analyst'] # only pinyin support
	model.database_init()
	core.GetQuickinfoList(keywords) 
	linklist = get_linklist()
	core.GetDetailList(linklist)
	c = dprocess.opendb()
#	dprocess.quickid(c) #replace Row to JHK to make sure both tables have same id's
#	msg1 = 'Done.'
#	msg2 = 'Check the results.'
#	ifttt_msg(msg1, msg2) # IFTTT cannot response the post request.

if __name__=="__main__":
	main()