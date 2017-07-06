#-*-coding: utf-8-*-

import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
import threading
from six.moves import urllib
import socket
import re
import math
import logging
import time

#logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
	{'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
	{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
	{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
	{'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
	{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
	{'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
	{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
	{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
	{'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
	{'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]



def get_source_code(url): # not sure if the while loop and exit strategy work well...
	i = 0
	while i<10: #while loop if error raises, try 10 times
		i += 1
		try:
			result = requests.get(url, headers=hds[random.randint(0,len(hds)-1)], timeout=(6,30))
			#result = requests.get(url, headers=hds)
			source_code = result.content
			if source_code is not None:
				break
		except Exception as e:
			logging.error(e)
			print(e)
			time.sleep(3)
			continue
	return source_code


def get_total_pages(url):
	source_code = get_source_code(url)
	soup = BeautifulSoup(source_code, 'lxml')
	try:
		page_info = soup.head.title.get_text()
	except Exception as e:
		page_info = None
		logging.error(e)
	
	pattern = r"\d+"
	sum = int(re.search(pattern, page_info).group())
	total_page = int(math.ceil(sum/50))
	return total_page

#===========proxy ip spider, we do not use now because it is not stable===========
proxys_src = []
proxys = []

def spider_proxyip():
	try:
		for i in range(1,4):
			url='http://www.xicidaili.com/nt/' + str(i)
			req = requests.get(url,headers=hds[random.randint(0, len(hds) - 1)])
			source_code = req.content
			soup = BeautifulSoup(source_code,'lxml')
			ips = soup.findAll('tr')

			for x in range(1,len(ips)):
				ip = ips[x]
				tds = ip.findAll("td")
				proxy_host = "http://" + tds[1].contents[0]+":"+tds[2].contents[0]
				proxy_temp = {"http":proxy_host}
				proxys_src.append(proxy_temp)
	except Exception as e:
		print ("spider_proxyip exception:")
		print (e)

def test_proxyip_thread(i):
	socket.setdefaulttimeout(5)
	url = "http://cq.lianjia.com"
	try:
		proxy_support = urllib.request.ProxyHandler(proxys_src[i])
		opener = urllib.request.build_opener(proxy_support)
		urllib.request.install_opener(opener)
		res = urllib.request.Request(url,headers=hds[random.randint(0, len(hds) - 1)])
		source_cod = urllib.request.urlopen(res,timeout=10).read()
		if source_cod.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') == -1:
			proxys.append(proxys_src[i])
	except Exception as e:
		return
	   # print(e)

def test_proxyip():
	print ("proxys before:"+str(len(proxys_src)))
	threads = []
	try:
		for i in range(len(proxys_src)):
			thread = threading.Thread(target=test_proxyip_thread, args=[i])
			threads.append(thread)
			thread.start()

		for thread in threads:
			thread.join()
	except Exception as e:
		print (e)
	print ("proxys after:" + str(len(proxys)))

def prepare_proxy():
	spider_proxyip()
	test_proxyip()

def readurl_by_proxy(url):
	try:
		tet = proxys[random.randint(0, len(proxys) - 1)]
		proxy_support = urllib.request.ProxyHandler(tet)
		opener = urllib.request.build_opener(proxy_support)
		urllib.request.install_opener(opener)
		req = urllib.request.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
		source_code = urllib.request.urlopen(req, timeout=10).read()
		if source_code.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') != -1:
			proxys.remove(tet)
			print('proxys remove by IP traffic, new length is:' + str(len(proxys)))
			return None

	except Exception as e:
		proxys.remove(test)
		print('proxys remove by exception:')
		print (e)
		print ('proxys new length is:' + str(len(proxys)))
		return None

	return source_code 
