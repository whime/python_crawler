#爬取句子迷网站龙族相关的经典语句
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import threading
import lxml
from fake_useragent import UserAgent


class sentenceCrawler:
	def __init__(self,linkList,ipList):
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
		self.ipList=ipList

	# 获取代理
	def get_random_proxies(self):
		proxy_list = []
		for ip in self.ipList:
			proxy_list.append('http://' + ip)
		proxy_ip = random.choice(proxy_list)
		proxies = {'https': proxy_ip}
		return proxies

	def CrawlOnePage(self,link,part):
		#请求延时
		self.sentenceBox=[]
		header={"User-Agent": random.choice(self.user_agent),
					  'Host':'www.juzimi.com',
					  'Referer':'https://www.juzimi.com/article/'}
		time.sleep(random.random()*3)
		proxies=self.get_random_proxies()
		print(proxies)
		res=requests.get(link,headers=header,proxies=proxies)
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
		for link in self.linkList:
			part=1
			proxies=self.get_random_proxies()
			print(proxies)
			#设置代理
			response=requests.get(link,headers=header,proxies=proxies)
			with open("dragon1.html",'w',encoding="utf-8") as ff:
				ff.write(response.text)
			# response.encoding='gbk'
			# print(response.text)
			soup=BeautifulSoup(response.text,"html.parser")
			lastPage=soup.select('.pager-last a')
			print(lastPage)

			lastPage=re.search(r'>(\d+)<',str(lastPage[0])).group(1)
			print(lastPage)
			# print(type(lastPage))
			pageSum=int(lastPage)
			self.CrawlOnePage(link,part)
			#IO密集型，使用多线程
			for i in range(1,pageSum):
				th=threading.Thread(target=self.CrawlOnePage,args=(link+"?page="+str(i),part))
				th.start()
			part+=1

#来源
def get_ip_list(url, headers):
		web_data = requests.get(url, headers=headers)
		soup = BeautifulSoup(web_data.text, 'lxml')
		ips = soup.find_all('tr')
		ip_list = []
		for i in range(1, len(ips)):
			ip_info = ips[i]
			tds = ip_info.find_all('td')
			ip_list.append(tds[1].text + ':' + tds[2].text)
		print(ip_list)
		print("\n")
		#可用性测试
		new_ip_list=[]
		for ip in ip_list:
			try:
				req=requests.get('https://www.baidu.com',proxies={'proxy':'http://'+ip})
				new_ip_list.append(ip)
				print("ok")
			except Exception as e:
				print(e)
		print(new_ip_list)
		return new_ip_list


if __name__ == '__main__':
	#需要爬取的五个链接
	# dragon1="https://www.juzimi.com/article/龙族"
	# dragon2="https://www.juzimi.com/article/26052"
	# dragon3="https://www.juzimi.com/article/%E9%BE%99%E6%97%8F3%C2%B7%E9%BB%91%E6%9C%88%E4%B9%8B%E6%BD%AE"
	# dragon4="https://www.juzimi.com/article/113093"
	# dragon5="https://www.juzimi.com/article/272635"
	linkList=[]

	dragon1="https://www.baidu.com"
	linkList.append(dragon1)
	# linkList.append(dragon2)
	# 	# linkList.append(dragon3)
	# 	# linkList.append(dragon4)
	# 	# linkList.append(dragon5)

	#获取代理ip列表
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
	ipList=get_ip_list('http://www.xicidaili.com/nn/1',headers=headers)
	sc=sentenceCrawler(linkList,ipList)
	# sc=sentenceCrawler(linkList)
	sc.startCrawl()

