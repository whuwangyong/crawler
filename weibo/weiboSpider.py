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
cookies = [{"Cookie": "_T_WM=564824bb1589a30e3d0c8bcf5fd27cc4; SUB=_2A251u8RkDeRxGeNI4lES9SnMzz2IHXVXR-wsrDV6PUJbkdBeLXbCkW1WKJ4IuwxGNab1HWT7TKk6dJeS_w..; SUHB=00xpAt8JDskW1i; SCF=AhRPKBxB-_WuWB_L5ur2Hkw_shAdVQezioscCczugtxqxD0_JKedWThYeFVXGj9Vln9nl5Di3bVgFmytNakUMNk.; SSOLoginState=1488958516"},
			{"Cookie": "_T_WM=fa11da29ec28c0458646e8f31e97814c; SUB=_2A251u7DiDeRxGeNI4lES9SjFzDSIHXVXR9CqrDV6PUJbkdBeLUKlkW2N7oC0JIlKSEGyMWLz-_LtwnAcPw..; SUHB=00xpAt8LDskWPO; SCF=AsqXmh5Cus6Y-3p8b7RtGda_bgOE1yhq-OSlAVMwt91nxxDQ_NXym5A4Jel7ZpwHJtBHINAM7f1AaVmv49ufcfc.; SSOLoginState=1488961714"},
			{"Cookie": "_T_WM=081a059345dc94e63c19b0f645bb2176; SUB=_2A251u7EQDeRxGeNI4lES9SjLzzmIHXVXR99YrDV6PUJbkdBeLWbFkW1SeZ8_k8hFqEUdDCE8FrSW6mCcSg..; SUHB=0u5RMC7VncECeZ; SCF=Aoc-8WCx9Z74mKLYJ034ery9zo5PKjkMPZMagR0xnYcs_kcsZKCm6EgDXgQ1zfU-kM0zfB2ltsklmfNMH2I8Oxs.; SSOLoginState=1488961856"},
			{"Cookie": "_T_WM=c551a3ab7151ea68dbfba50f6fad3d1d; SUB=_2A251u7E3DeRxGeNI4lES9SjKzjWIHXVXR99_rDV6PUJbkdBeLVDbkW1FA_9xkHxfNPGoHNdbOxyrwks4yw..; SUHB=02MfGS_nXI2J4W; SCF=AmCXL0hgX4k1RZo7nzdTwd6v9wjVWPKtid3z6cWEs2la_mihsCf1Q2nbAhMcJYighiibdbkmzjuU1dpfjlraNxE.; SSOLoginState=1488961895"},
			{"Cookie": "_T_WM=43beb11eee50a9c705ff299239ce3268; SUB=_2A251u7HcDeRxGeNI4lES9SjJzTSIHXVXR9-UrDV6PUJbkdBeLWatkW0ROllUTi5qxELE3m-xvIEopXUAuA..; SUHB=0Jvg9a5fAfOvw_; SCF=AhcIzb7s2ScIrKsbsc_jimxsLpwlrbgwLoUxSAL7Ioo_n-RDH8R4TrKpSjcSPhqQtha0tbCEggURKD_LPvp9ukA.; SSOLoginState=1488961932"}]

def getTotalPage():
	url = 'http://weibo.cn/u/%d?page=1&is_all=1'%user_id
	html = requests.get(url, cookies=random.choice(cookies)).content
	selector = etree.HTML(html)
	pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
	return pageNum

def getStartPage(start, end):
	mid = int((start+end)/2)
	url = 'http://weibo.cn/u/%d?page=%d&is_all=1'%(user_id,mid)
	html_doc = requests.get(url, cookies = random.choice(cookies)).content;
	soup = BeautifulSoup(html_doc,"lxml")
	weibo = soup.find_all("div", class_="c")[0]
	mytime = weibo.find("span",class_="ct")
	if mytime is not None:
		if re.match(r'2016-12', mytime.get_text()):
			return mid
		if re.match(r'(\d\d月\d\d日)|今天', mytime.get_text()):# 2017
			return getStartPage(mid, end)
		if re.match(r'(201[012345]-)|2016-0[1-9]|2016-1[01]', mytime.get_text()): # 2010~2015, 2016.01~2016.11
			return getStartPage(start, mid)
	time.sleep(1)

	
def crawl():
	cnt = 1
	total = getTotalPage()
	start = getStartPage(1, total)
	for page in range(start, total):
		time.sleep(random.randint(1,3))
		url = 'http://weibo.cn/u/%d?page=%d&is_all=1'%(user_id,page)
		html_doc = requests.get(url, cookies = random.choice(cookies)).content;
		soup = BeautifulSoup(html_doc,"lxml")
		for weibo in soup.find_all("div", class_="c"):
			context = weibo.find("span",class_="ctt")
			attitude = weibo.find("a",href=re.compile("http://weibo.cn/attitude/*")) # 点赞数
			repost = weibo.find("a",href=re.compile("http://weibo.cn/repost/*")) # 转发数
			comment = weibo.find("a",href=re.compile("http://weibo.cn/comment/*")) # 评论数
			mytime = weibo.find("span",class_="ct") # 微博小尾巴

			# 只要2016年的数据
			if mytime is not None:
				if re.match(r'\d\d月\d\d日', mytime.text) is not None:
					continue # 跳过2017年的微博
				if re.match(r'2015-',mytime.text) is not None:
					return # 爬到2015年时返回
		
			if context is not None and attitude is not None and repost is not None and comment is not None:
				print(cnt,':',context.text, attitude.text, repost.text, comment.text, mytime.text)
				cnt += 1

if __name__ == '__main__':
	crawl()

