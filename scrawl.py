import core
import model
from model import quickinfo
import datetime
import requests

def get_linklist():
	res = []
	for info in quickinfo.select().where(quickinfo.updatetime>=datetime.datetime.combine(datetime.date.today(), datetime.time.min)):
		res.append(info.link)
	return res

def ifttt_msg(msg1, msg2):
	report={}
	report['value1'] = msg1
	report['value2'] = msg2
	requests.post("https://maker.ifttt.com/trigger/crawl/with/key/gJ3YX4tfFuB2C-2ZJp4W",data=report)

def main():
	keywords = [u'data+analyst',u'business+analyst'] # only pinyin support
#	keywords = [u'data+analyst']
	model.database_init()
	core.GetQuickinfoList(keywords) 
	linklist = get_linklist() 
	core.GetDetailList(linklist)
	msg1 = 'Done.'
	msg2 = 'Check the results.'
#	ifttt_msg(msg1, msg2)

if __name__=="__main__":
	main()