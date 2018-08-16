# -*- coding: utf-8 -*-
# coding=utf-8
"""
Created on Mon Aug 13 11:10:39 2018

@author: 95647
"""
import urllib
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import pymysql
from mytictoc import tic, toc

tic()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password="123456", db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE douban_books")  
def store(bookname,publication, comments, num, brief):
    cur.execute(r"""INSERT INTO literary_books (title, publisher,rating,comments_num,brief) VALUES ("%s","%s","%s","%s","%s")""",(bookname
                , publication, comments, num, brief))
    cur.connection.commit()

types=input("请输入需要爬虫的书籍类别，包括：小说、历史、文学、中国文学、外国文学、\
随笔、散文、推理、文化、社会等等；具体类别见网站：https://book.douban.\
com/tag/?view=type&icn=index-sorttags-all, ------输入------>：")
for i in range(0,50):
    if i ==0 :
        url = "https://book.douban.com/tag/%s"%types
    else:
        pages = i*20
        url = "https://book.douban.com/tag/%s?start=%s&type=T"%(types,str(pages))
    s = quote(url,safe=string.printable)
    req = urllib.request.Request(s, headers=headers)
    html = urlopen(req)
    bsObj = BeautifulSoup(html,'lxml')
    items = bsObj.findAll("li",class_="subject-item")
    for item in items:
        titles = item.find("a",title = re.compile(".*")).contents
        if len(titles)> 1 :
            bookname = str(titles[0].strip()) + str(titles[1].text.strip())
        else:
            bookname = titles[0].strip()
        publication =item.find("div",class_="pub").get_text().strip()
        try: 
            comments = float(item.find("span", class_="rating_nums").text.strip())
        except AttributeError as e:
            commnets = 0
        try:
            num = item.find("span", class_="pl").text.strip()
        except AttributeError as e:
            num = "0"
        try:
            brief = item.p.text.strip()
        except AttributeError as e:
            brief = "None"
        store(bookname, publication, comments, num, brief)

cur.close()
conn.close()  #try...finally 确保循环程序就算是出现错误，也能正常的关闭MYSQL连接和游标
toc()  #this scarpy use of total time
