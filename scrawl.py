import core
import model
from model import quickinfo
import datetime

def get_linklist():
	res = []
	for info in quickinfo.select().where(quickinfo.updatetime>=datetime.datetime.combine(datetime.date.today(), datetime.time.min)):
		res.append(info.link)
	return res

if __name__=="__main__":
	keywords = [u'data+analyst',u'business+analyst'] # only pinyin support
	model.database_init()
	core.GetQuickinfoList(keywords) # Init,scrapy celllist and insert database; could run only 1st time
	linklist = get_linklist() # Read celllist from database
	core.GetDetailList(linklist)