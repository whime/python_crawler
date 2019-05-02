import requests
from bs4 import BeautifulSoup
import re
import time
import random
import threading

"""
爬取句子迷网站龙族1-5部相关的经典语句，使用了代理ip进行反反爬虫
author:whime
date:19:02 2019/05/02
"""

class sentenceCrawler:
	def __init__(self,linkList):
		self.linkList=linkList
		self.sentenceBox=[]
		self.user_agent=[
			'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
		]
		self.skipNum=0


	#使用阿布云代理，代码来自使用文档
	def get_random_proxies(self):
		# 要访问的目标页面
		# targetUrl = "http://test.abuyun.com"
		#targetUrl = "http://proxy.abuyun.com/switch-ip"
		#targetUrl = "http://proxy.abuyun.com/current-ip"

		# 代理服务器
		proxyHost = "http-dyn.abuyun.com"
		proxyPort = "9020"

		# 代理隧道验证信息
		proxyUser = "H39L72OKP3EM20RD"
		proxyPass = "BC526B1680FA2DFD"

		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
		  "host" : proxyHost,
		  "port" : proxyPort,
		  "user" : proxyUser,
		  "pass" : proxyPass,
		}

		proxies = {
			"http"  : proxyMeta,
			"https" : proxyMeta,
		}
		return proxies
		# resp = requests.get(targetUrl, proxies=proxies)
		# print(resp.status_code)
		# print(resp.text)

	def CrawlOnePage(self,link,part):
		#请求延时
		self.sentenceBox=[]
		header={"User-Agent": random.choice(self.user_agent),
					  'Host':'www.juzimi.com',
					  'Referer':'https://www.juzimi.com/article/'}
		time.sleep(5)
		proxies=self.get_random_proxies()
		print(proxies)
		try:
			#出现chunked编码和http.client.IncompleteRead问题，直接忽略跳过。。。
			#https://blog.csdn.net/wangzuxi/article/details/40377467
			#https://www.programcreek.com/python/example/9517/httplib.IncompleteRead%20%E5%A4%84%E7%90%86%E6%96%B9%E5%BC%8F%E6%9D%A5%E6%BA%90
			#也有说可以使用http/1.0解决  https://blog.csdn.net/haoli001/article/details/40863433
			res=requests.get(link,headers=header,proxies=proxies)
		except Exception as e:
			self.skipNum+=1
			return
		print(res.status_code)
		soup=BeautifulSoup(res.text,"html.parser")
		for viewField in soup.select(".xlistju"):
			# print(viewField.text)
			self.sentenceBox.append(viewField.text+"\n")
		with open("dragon"+str(part)+".txt",'a',encoding='utf-8') as f:
				for sentence in self.sentenceBox:
					f.write(sentence+"\n")
				f.write("\n\n\n")
		print(link)

	def startCrawl(self):
		header={"User-Agent": random.choice(self.user_agent),
					  'Host':'www.juzimi.com',
					  'Referer':'https://www.juzimi.com/article/'}
		part=1
		for link in self.linkList:

			proxies=self.get_random_proxies()
			print(proxies)
			#设置代理
			response=requests.get(link,headers=header,proxies=proxies)
			soup=BeautifulSoup(response.text,"html.parser")
			lastPage=soup.select('.pager-last a')

			lastPage=re.search(r'>(\d+)<',str(lastPage[0])).group(1)

			pageSum=int(lastPage)
			print("dragon"+str(part)+"有"+str(pageSum)+"页。")
			self.CrawlOnePage(link,part)

			for i in range(1,pageSum):
				#使用的是阿布云代理ip，限制每秒请求次数，无法多线程，并且每次延缓请求1s，慢慢爬
				# th=threading.Thread(target=self.CrawlOnePage,args=(link+"?page="+str(i),part))
				self.CrawlOnePage(link+"?page="+str(i),part)
				# th.start()
			print("dragon"+str(part)+"  done")
			part+=1




if __name__ == '__main__':
	#需要爬取的五个链接主页
	dragon1="https://www.juzimi.com/article/龙族"
	dragon2="https://www.juzimi.com/article/26052"
	dragon3="https://www.juzimi.com/article/%E9%BE%99%E6%97%8F3%C2%B7%E9%BB%91%E6%9C%88%E4%B9%8B%E6%BD%AE"
	dragon4="https://www.juzimi.com/article/113093"
	dragon5="https://www.juzimi.com/article/272635"
	linkList=[]


	linkList.append(dragon1)
	linkList.append(dragon2)
	linkList.append(dragon3)
	linkList.append(dragon4)
	linkList.append(dragon5)


	sc=sentenceCrawler(linkList)
	sc.startCrawl()
	print("总共跳过了"+str(sc.skipNum))

