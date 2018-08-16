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
import pandas as pd
import string
from mytictoc import tic, toc

tic()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
url = "https://book.douban.com/tag/历史"
s = quote(url,safe=string.printable)
req = urllib.request.Request(s, headers=headers)
html = urlopen(req)
# print(html.read().decode("utf-8"))
bsObj = BeautifulSoup(html,'lxml')
items = bsObj.findAll("li",class_="subject-item")
book_info = []
for item in items:
    info = []
    titles = item.find("a",title = re.compile(".*")).contents
    if len(titles)> 1 :
        bookname = str(titles[0].strip()) + str(titles[1].text.strip())
    else:
        bookname = titles[0].strip()
    publication =item.find("div",class_="pub").get_text().strip()
    comments = item.find("span", class_="rating_nums").text.strip()
    num = item.find("span", class_="pl").text.strip()
    brief = item.p.text.strip()
    info.append(bookname)
    info.append(publication)
    info.append(comments)
    info.append(num)
    info.append(brief)
    book_info.append(info)
    
column = ["书名","出版社","评分","参与人数","内容简介"]
all_books_info = pd.DataFrame(columns=column ,data= book_info)
all_books_info.to_csv(r"""C:\Users\95647\Desktop\douban_books.csv""")
toc()  #this scarpy use of total time
