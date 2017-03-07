#!/usr/bin/python3

import urllib.request
import os
import time
import random
import re
import pymysql

from bs4 import BeautifulSoup

def url_open(url):
    req1 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.0'})
    req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.1'})
    req3 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.2'})
    req4 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.3'})
    req5 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.4'})
    req6 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.5'})
    req7 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req8 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.1'})
    req_list = [req1, req2,req3, req4, req5, req6,req7, req8]
    response = urllib.request.urlopen(random.choice(req_list))
    html = response.read()
    # print ('url_open done!')
    return html


def get_info():
    conn = pymysql.connect(host='localhost', user='root', password='root', database='test',charset='utf8')
    cursor = conn.cursor()
    cursor.execute('''drop table if exists offershow;
        CREATE TABLE offershow (
            id int unsigned NOT NULL AUTO_INCREMENT,
            company varchar(100),
            position varchar(100),
            city varchar(50),
            salary TEXT,
            score int DEFAULT 0,
            createdate date, 
            remark TEXT,
            pageviews int default 0,
            PRIMARY KEY (id)
        ) ENGINE=MyISAM charset=utf8 AUTO_INCREMENT=1;
        create unique index id on offershow(id);''')


    prefix = str(time.localtime().tm_year) + '-' \
        + str(time.localtime().tm_mon) + '-' \
        + str(time.localtime().tm_mday)
    f = open(prefix+'-insert.sql', 'w')


    for page in range(1,918):

        if page%3 == 0:
            time.sleep(0.04)

        s=[]
        url = "http://www.ioffershow.com:8000/offerdetail/"+str(page)
        html_doc = url_open(url);
        soup = BeautifulSoup(html_doc,"lxml")
        j=0
        for item in soup.find_all("p", align="center"):
            j += 1
            if j%2 ==1:
                continue
            if item is None:
                s.append("")
            else:
                s.append(item.string)

        pv=soup.find_all("h1")
        if len(pv)==0:
            continue
        pv=re.findall( "\d+", pv[0].string)
        if len(pv)==0:
            continue
        s.append(pv[0])
        print("#"+str(i)+":\t"+ str(s))
        sqlstr = "insert into offershow values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s');\n" \
            %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7])
        try:
            cursor.execute(sqlstr)
            f.write(sqlstr)
        except:
            print("----------------- cursor.execute(sqlstr) error! -------------------")
    f.close()

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    get_info()

