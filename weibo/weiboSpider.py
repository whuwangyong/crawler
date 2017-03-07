#-*- coding:utf8 -*-
#!/usr/bin/python3

import requests
import os
import sys
import time
import random
import re
from lxml import etree

from bs4 import BeautifulSoup

if(len(sys.argv) >=2):
	user_id = (int)(sys.argv[1])
else:
	user_id = (int)(raw_input('input user_id:'))

# cookie = {"Cookie": "your cookie"}
cookie = {"Cookie": "_T_WM=7d8589545efb4f1781f62badbec29c5f; SCF=AjT2EBERMtcl4ILh1ypMsWjpDQlN5t7V8Lrp-57YaCyae7Oe4gieEjbQaoaEYFofp5WJA5qSkh-Nite5F2ZhWt8.; SUB=_2A251uurJDeTxGedJ7FsX8ijLzTyIHXVXRPaBrDV6PUJbkdBeLXnEkW0_jzJbRPEmWCgsB3aJhY2WwArzYQ..; SUHB=04W_Qya1o4yeor; SSOLoginState=1488886425"}

def getTotalPage():
	url = 'http://weibo.cn/u/%d?page=1&is_all=1'%user_id
	html = requests.get(url, cookies=cookie).content
	selector = etree.HTML(html)
	pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
	return pageNum
	
def crawl():
	cnt = 1
	for page in range(1, getTotalPage()):
		time.sleep(1)
		url = 'http://weibo.cn/u/%d?page=%d&is_all=1'%(user_id,page)
		html_doc = requests.get(url, cookies = cookie).content;
		soup = BeautifulSoup(html_doc,"lxml")
		for weibo in soup.find_all("div", class_="c"):
			context = weibo.find("span",class_="ctt")
			attitude = weibo.find("a",href=re.compile("http://weibo.cn/attitude/*")) # 点赞数
			repost = weibo.find("a",href=re.compile("http://weibo.cn/repost/*")) # 转发数
			comment = weibo.find("a",href=re.compile("http://weibo.cn/comment/*")) # 评论数
			mytime = weibo.find("span",class_="ct") # 微博小尾巴
		
			if context is not None and attitude is not None and repost is not None and comment is not None:
				print(cnt,':',context.text, attitude.string, repost.string, comment.string, mytime.string)
				cnt += 1

if __name__ == '__main__':
	crawl()

