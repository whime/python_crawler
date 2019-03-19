# -*-coding;utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import jieba
from wordcloud import WordCloud
import PIL.Image as Image
import numpy as np

#爬取中药名称并做词云
#参考https://mp.weixin.qq.com/s?__biz=MzU4NjUxMDk5Mg==&mid=2247485327&idx=1&sn=1f4fc09ecef0fb7fc0ca4ba52e11a0a6&chksm=fdfb6070ca8ce966b1c6e470b5a6121d08287c328a9af66be379ec478bf5f5f9184cd05115f2&scene=0&xtrack=1#rd
class name_crawler:
	def __init__(self):
		self.medicine_names=[]
		self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	def getExtraName(self,link_List):
		for link in link_List:
			res=requests.get(link,headers=self.headers)
			res.encoding='gbk'
			soup=BeautifulSoup(res.text,'html.parser')
			html=soup.select('.art_1')
			html=html[0].text.replace('\n','').replace('\t','').strip()

			result=[]
			if re.search('【别名】.*?【英文名】',html) is not None:
				#获取别名内容
				extraNames=re.search('【别名】.*?【英文名】',html).group()[4:-8]
				self.medicine_names.extend(extraNames.split('、'))
	def genWordCloud(self):
		text="".join(self.medicine_names)
		words=jieba.lcut(text,cut_all=True)#jieba分词全模式
		words=" ".join(words)#使用空格分开

		#词云的遮罩层
		mask=np.array(Image.open("love.jpg"))
		wc=WordCloud(min_font_size=10,height=2000,width=2000,mask=mask,background_color="white",font_path = "C:\Windows\Fonts\STXINGKA.TTF").generate(words)
		pic=wc.to_image()
		pic.show()
		wc.to_file("medicine_cloud.jpg")

	def  startCrawl(self,n):#传入要爬取的页面数量
		pageNum=n
		page_links=[]	#所有页的页内链接，指向该药物的详细信息
		for j in range(1,pageNum+1):
			response=requests.get('http://m.zhongyoo.com/name/page_'+str(j)+'.html',headers=self.headers)
			#缺少此句输出中文会乱码
			response.encoding='gbk'

			soup=BeautifulSoup(response.text,'html.parser')
			# print(soup.prettify())
			#正则表达式匹配链接
			pattern=re.compile(r'http:.*?.html')
			page_links.extend(pattern.findall(soup.prettify()))
			# print(page_links)

			for i in soup.select('.t strong'):
				self.medicine_names.append(i.text)

		#将中药名称和链接写入文件
		#一次写入
		with open('name_links.txt','w',encoding='utf-8') as ft:
			#使用zip才可以对不同列表进行分别遍历
			for i,j in zip(self.medicine_names,page_links):
				ft.write(i+"		"+j+'\n')

		#访问链接里的页面取出中药别名
		name_crawler.getExtraName(self,page_links)
		print('爬取了'+str(len(self.medicine_names))+'个名称')
		name_crawler.genWordCloud(self)




		# print(len(medicine_names))
if __name__ == '__main__':
	nc=name_crawler()
	res=requests.get("http://m.zhongyoo.com/name/",headers=nc.headers)
	res.encoding='gbk'
	soup=BeautifulSoup(res.text,'html.parser')
	#爬取下方导航按钮获取总页数
	navigate_link=soup.select('.page_c a')
	# print(type(navigate_link[2]['href']))	#访问属性href
	#获取到最后一页的页码
	last_page=re.search('\d+',navigate_link[2]['href']).group()
	last_page=int(last_page)
	pageSum=int(input("输入要爬取的页面数量(总共%d页)："%last_page))
	while pageSum>last_page:
		print("请输入正确的页数！")
		pageSum=int(input("输入要爬取的页面数量(总共%d页)："%last_page))

	print("start crawl...")
	nc.startCrawl(pageSum)
	print("crawl success!")
	print("end crawl...")
