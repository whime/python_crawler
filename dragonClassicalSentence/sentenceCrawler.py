#爬取句子迷网站龙族相关的经典语句
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from fake_useragent import UserAgent


"""TODO	应该是被反爬了,浏览器都访问不了"""
class sentenceCrawler:
	def __init__(self,linkList):
		self.linkList=linkList
		self.sentenceBox=[]
		self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


	def CrawlOnePage(self,link):
		time.sleep(random.random()*3)
		res=requests.get(link)
		print(res.status_code)
		soup=BeautifulSoup(res.text,"html.parser")
		for viewField in soup.select(".views-field-phpcode-1 a"):
			print(viewField.text)
			self.sentenceBox.append(viewField.text+"\n")
		print("anotherPage!")

	def startCrawl(self):
		for link in self.linkList:
			part=1
			response=requests.get(link)
			with open("dragon1.html",'w',encoding="utf-8") as ff:
				ff.write(response.text)
			# response.encoding='gbk'
			# print(response.text)
			soup=BeautifulSoup(response.text,"html.parser")
			lastPage=soup.select('.pager-last a')
			print(lastPage)

			lastPage=re.search(r'>(\d+)<',str(lastPage[0])).group(1)
			print(lastPage)
			print(type(lastPage))
			pageSum=int(lastPage)
			self.CrawlOnePage(link)
			for i in range(1,pageSum):
				self.CrawlOnePage(link+"?page="+str(i))
			with open("dragon"+str(part)+".txt",'w',encoding='utf-8') as f:
				for sentence in self.sentenceBox:
					f.write(sentence)
			part+=1
			self.sentenceBox=[]



if __name__ == '__main__':
	#需要爬取的五个链接
	dragon1="https://www.juzimi.com/article/龙族1"
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

