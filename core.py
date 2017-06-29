#-*-coding: utf-8-*-

from bs4 import BeautifulSoup
import model
import misc
from misc import ifttt_msg
import time
import datetime
import logging
import re

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
BASE_URL = u"http://hk.jobsdb.com/HK/en/Search/FindJobs?AD=30&Blind=1&Host=J&JobCat=1&JSRV=1&Key=%s&KeyOpt=COMPLEX&SearchFields=Positions%%2cCompanies&page=%d"
pg_no = 0

def GetQuickinfoList(keywords): 
	logging.info("Get Jobs Quick Infomation")
	starttime = datetime.datetime.now()
	for keyword in keywords:
		try:
			get_lists_perword(keyword)
			logging.info(keyword + "Done")
		except Exception as e:
			logging.error(e)
			logging.error(keyword + "Fail")
			pass
	endtime = datetime.datetime.now()
	logging.info("Run time: " + str(endtime - starttime))

def GetDetailList(linklist):
	logging.info("Get House Infomation")
	starttime = datetime.datetime.now()
	for link in linklist:
		try:
			get_detail_perlink(link)
			logging.info(link + "Done")
		except Exception as e:
			logging.error(e)
			logging.error(link + "Fail")
			pass
	endtime = datetime.datetime.now()
	logging.info("Run time: " + str(endtime - starttime))

def get_lists_perword(keyword):
	url = BASE_URL % (keyword, pg_no)
	source_code = misc.get_source_code(url)
	soup = BeautifulSoup(source_code, 'lxml')

	total_pages = misc.get_total_pages(url)
	
	if total_pages == None:
		row = model.quickinfo.select().count()
		raise RuntimeError("Finish at %s because total_pages is None" % row)

	for page in range(total_pages):
		url_page = BASE_URL % (keyword, page)
		source_code = misc.get_source_code(url_page)
		soup = BeautifulSoup(source_code, 'lxml')

		itemList = soup.findAll("div", {"class":"result-sherlock-cell"})
		i = 0

		for item in itemList: 
			i = i + 1
			info_dict = {}
			try:
				id = item.get('id')
				info_dict.update({u'id':id})

				link_title = item.find("h3", {"class":"job-title"})
				info_dict.update({u'title':link_title.get_text()})
				info_dict.update({u'link':link_title.a.get('href')})

				descriptions = item.find("li", {"class":"description"})
				summary_list = [desc.get_text() for desc in descriptions]
				summary = ' | '.join(summary_list)
				info_dict.update({u'summary':summary})

				date = item.find("div", {"class":"job-quickinfo"}).meta,get('content')
				info_dict.update({u'postdate':date})
				
				wage = item.find('p',{'class':'job-quickinfo-salary'}).get_text()
				info_dict.update({u'salary':wage})
			except:
				continue
			# quickinfo insert into database
			model.quickinfo.insert(**info_dict).upsert().execute()
			time.sleep(5)

def get_detail_perlink(link): 
	url = link
	source_code = misc.get_source_code(url)
	soup = BeautifulSoup(source_code, 'lxml')

	try:
		communitytitle = name.find("div", {"class":"title"})
		info_dict.update({u'title':communitytitle.get_text().strip('\n')})
		info_dict.update({u'link':communitytitle.a.get('href')})

		district = name.find("a", {"class":"district"})
		info_dict.update({u'district':district.get_text()})
		bizcircle = name.find("a", {"class":"bizcircle"})
		info_dict.update({u'bizcircle':bizcircle.get_text()})

		tagList = name.find("div", {"class":"tagList"})
		info_dict.update({u'tagList':tagList.get_text().strip('\n')})
	except:
		continue
	# communityinfo insert into mysql
	model.Community.insert(**info_dict).upsert().execute()

	time.sleep(5)

def check_block(soup):
	if soup.title.string == "414 Request-URI Too Large":
		logging.error("Lianjia block your ip, please verify captcha manually at lianjia.com")
		return True
	return False