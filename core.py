#-*-coding: utf-8-*-

from bs4 import BeautifulSoup
import model
from model import quickinfo
from model import detailinfo
import misc
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
			logging.info(keyword + "   Done")
		except Exception as e:
			logging.error(e)
			logging.error(keyword + "   Fail")
			pass
	endtime = datetime.datetime.now()
	logging.info("Run time: " + str(endtime - starttime))

def GetDetailList(linklist):
	logging.info("Get Detail Infomation")
	starttime = datetime.datetime.now()
	for link in linklist:
		try:
			get_detail_perlink(link)
			logging.info(link[0] + "   Done")
		except Exception as e:
			logging.error(e)
			logging.error(link[0] + "   Fail")
			continue
	endtime = datetime.datetime.now()
	logging.info("Run time: " + str(endtime - starttime))

def get_lists_perword(keyword):
	url = BASE_URL % (keyword, pg_no)
	total_pages = misc.get_total_pages(url)
	print('The total pages number is: ', total_pages)
	time.sleep(3)
	
	if total_pages == None:
		row = model.quickinfo.select().count()
		raise RuntimeError("Finish at %s because total_pages is None" % row)

	for page in range(total_pages):
		url_page = BASE_URL % (keyword, page)
		source_code = misc.get_source_code(url_page)
		soup = BeautifulSoup(source_code, 'lxml')

		itemList = soup.findAll("div", {"class":"result-sherlock-cell"})
		print('The items are: ', len(itemList))

		for item in itemList: 
			info_dict = {}
			try:
				id = item.get('id')
				info_dict.update({'id':id})

				link_title = item.find("h3", {"class":"job-title"})
				info_dict.update({'title':link_title.get_text()})
				info_dict.update({'link':link_title.a.get('href')})

				if item.find("li", {"itemprop":"description"}):
					descriptions = item.findAll("li", {"itemprop":"description"})
					summary_list = [desc.get_text() for desc in descriptions]
					summary = ' | '.join(summary_list)
					info_dict.update({'summary':summary})
				else:
					info_dict.update({'summary':'no description'})
				
				if item.find('p',{'class':'job-quickinfo-salary'}):
					wage = item.find('p',{'class':'job-quickinfo-salary'}).get_text()
					info_dict.update({'salary':wage})
				else:
					info_dict.update({'salary':'not specified'})
				
				date = item.find("div", {"class":"job-quickinfo"}).meta.get('content')
				info_dict.update({'postdate':date})
				
				label = keyword.replace('+',' ')
				info_dict.update({'label':label})
#				print(info_dict)

			except:
#				print('There is no item found')
				continue
			quickinfo.insert(**info_dict).upsert().execute()
		time.sleep(5)


def get_detail_perlink(link): 
	url = link[0]
	label = link[1]
	source_code = misc.get_source_code(url)
	soup = BeautifulSoup(source_code, 'lxml')
	info_dict = {}
	
	try:
		ref_content = soup.find('p',{'class':'data-ref ref-jobsdb'}).get_text()
		ref_pattern = r"JHK\d+"
		ref = re.search(ref_pattern, ref_content).group()
		info_dict.update({'ref':ref})
		
		title = soup.find('h1',{'itemprop':'title'}).get_text()
		info_dict.update({'title':title})
		
		info_dict.update({'link':link})
		
		datePosted = soup.find('p',{'itemprop':'datePosted'}).get_text()
		info_dict.update({'datePosted':datePosted})
		
		if soup.find('div',{'itemprop':'responsibilities'}):
			resp = soup.find('div',{'itemprop':'responsibilities'})
			resp_children = resp.findAll('li')
			resp_list = [resp.get_text() for resp in resp_children]
			responsibilities = ' | '.join(resp_list)
			info_dict.update({'Responsibilities':responsibilities})
		else:
			info_dict.update({'Responsibilities':'not specified'})
		
		if soup.find('div',{'itemprop':'requirements'}):
			req = soup.find('div',{'itemprop':'requirements'})
			req_children = req.findAll('li')
			req_list = [req.get_text() for req in req_children]
			requirements = ' | '.join(req_list)
			info_dict.update({'Requirements':requirements})
		else:
			info_dict.update({'Requirements':'not specified'})
		
		if soup.find('b',{'class':'primary-meta-lv'}):
			level = soup.find('b',{'class':'primary-meta-lv'}).get_text()
			info_dict.update({'CareerLevel':level})
		else:
			info_dict.update({'CareerLevel':'not specified'})
		
		if soup.find('b',{'class':'primary-meta-exp'}):
			years = soup.find('b',{'class':'primary-meta-exp'}).get_text()
			info_dict.update({'Exp':years})
		else:
			info_dict.update({'Exp':'not specified'})
		
		if soup.find('span',{'itemprop':'educationRequirements'}):
			qualification = soup.find('span',{'itemprop':'educationRequirements'}).get_text()
			info_dict.update({'Qualification':qualification})
		else:
			info_dict.update({'Qualification':'not specified'})
		
		if soup.find('span',{'id':'salaryTooltip'}):
			salary = soup.find('span',{'id':'salaryTooltip'}).get_text()
			info_dict.update({'salary':salary})
		else:
			info_dict.update({'salary':'not specified'})
		
		info_dict.update({'label':label})
	except:
		print('The item is not found')
	
	detailinfo.insert(**info_dict).upsert().execute()

	time.sleep(5)

# Not used in this section
def check_block(soup):
	if soup.title.string == "414 Request-URI Too Large":
		logging.error("Lianjia block your ip, please verify captcha manually at lianjia.com")
		return True
	return False