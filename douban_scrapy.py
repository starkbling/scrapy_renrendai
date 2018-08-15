# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 11:10:39 2018

@author: 95647
"""
from selenium import webdriver
import time
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options  #headless browser login ini
import requests
from pandas import DataFrame
# from mytictoc import tic, toc
# tic()

#driver = webdriver.PhantomJS(executable_path=r'''C:\Users\95647\Desktop\小工具\phantomjs-2.1.1-windows\bin\phantomjs.exe''')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#headers according to push F12 in browser
#defin a def to annalys of website
#use the login information you have signed
username = "13260282939"          #username
password = u"13756250324xll"     #password
#driver = webdriver.Firefox()  #use firefox to login in

#use headless browser to log
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options) 



def parse_html(i): 
    url = "http://www.we.com/lend/loanList!json.action?pageIndex=%s&"%i 
    #real resourse of data （<strong>Request <a href="URL:http://www.we.com/lend/loanList!json.action?pageIndex=2&_=1474379219318">URL</a></strong>） 
    resp=requests.get(url,headers=headers) #get html
    html=resp.json()  #resolve json file
    data=pd.DataFrame(html['data']['loans'])
    data.to_csv('loans%s.csv' % i) #resolved data write into csv file
    print("%s successsed" % i)
    
    
def LoginRRD(username, password):
    try:
        print(u'ready loging renrendai website...')
        driver.get("https://www.we.com/pc/passport/index/login")
        elem_user = driver.find_element_by_name("j_username")
        elem_user.send_keys(username)
        time.sleep(2)
        elem_pwd = driver.find_element_by_name("j_password")
        elem_pwd.send_keys(password)
        time.sleep(5)
        driver.find_element_by_xpath(r"""//*[@id="form-login"]/div/div[2]""").click()
        time.sleep(10) #set sleep time in order to save cookies
        print(u'login successful!')

    except Exception as e:
        print("Error:", e)
    finally:
        print(u'End Login!\n')
loanid_e =[]
def parse_userinfo(loanid,idx): #defin def to analysis borrower informations
    global loanid_e
#    global info
#    print(str(loanid))
    urll="https://www.renrendai.com/loan-%s.html"%str(loanid)  
    driver.get(urll)
    html = BeautifulSoup(driver.page_source,'lxml')
#    print(html.decode('utf-8'))
#    f= open("html0.txt","w")
#    f.write(html.decode("utf-8").replace('\xa9',"@"))    
#    f.close
    info = html.findAll('div',class_="borrower-info")
    userinfo = {}
    try:
        items = info[0].findAll('span',{"class":"pr20"})
    except IndexError as e:
        LoginRRD(username, password)
        loanid_e.append(loanid)
    else:    
        for item in items:
            var = item.get_text()
            value = item.parent.text.replace(var,"")
            userinfo[var]=value
        data = pd.DataFrame(userinfo,index=[idx])            
    return data

def get_loanId():
    table=DataFrame(np.array(['allowAccess', 'amount', 'amountPerShare', 'beginBidTime', 'borrowerId',
                              'borrowerLevel', 'currentIsRepaid', 'displayLoanType', 'finishedRatio',
                              'forbidComment', 'interest', 'interestPerShare', 'leftMonths', 'loanId',
                              'loanType', 'months', 'nickName', 'oldLoan', 'openTime', 'overDued',
                              'picture', 'principal', 'productId', 'readyTime', 'repaidByGuarantor',
                              'startTime', 'status', 'surplusAmount', 'title', 'utmSource']).reshape(1,30),columns=['allowAccess',
        'amount', 'amountPerShare', 'beginBidTime', 'borrowerId',
        'borrowerLevel', 'currentIsRepaid', 'displayLoanType', 'finishedRatio',
        'forbidComment', 'interest', 'interestPerShare', 'leftMonths', 'loanId',
        'loanType', 'months', 'nickName', 'oldLoan', 'openTime', 'overDued',
        'picture', 'principal', 'productId', 'readyTime', 'repaidByGuarantor',
        'startTime', 'status', 'surplusAmount', 'title', 'utmSource'])#网页源码获取
    i=1
    for i in range(1,101):    #101 is the last page 
        url = "https://www.renrendai.com/loan/list/loanList?startNum=%s&limit=10"%str(i) #resourse of data
        resp=requests.get(url,headers=headers) #get page information
        html=resp.text 
        data_dic = json.loads(html)
        data=DataFrame(data_dic['data']['list'])
        table=pd.concat([table,data])
        i += 1
    #save file
    table.to_csv('人人贷.csv',header=False) #csv
    loanId=table['loanId']
    return loanId

LoginRRD(username, password) #login renrendai
loanId = get_loanId()     #get loanid 
user_info=['neckname', 'credict_comit', 'name', 'id_card_num', 'academic',
           'marriage', 'loans', 'credict_limit', 'over_due_bill',
           'in_credict', 'total_borrow', 'over_due_times', 'repayment_times', 'principal_interest',
           'yzyq', 'aslary', 'house_estates', 'house_loan', 'car_asset', 'car_loan',
           'else', 'company_industry', 'company_scale', 'post', 'city',
           'career']
table2 = pd.DataFrame(np.array(user_info).reshape(1, 27), columns=user_info)


i = 1
idx = 0 
for loanid in loanId[1:10]:
    table2 = pd.concat([table2, parse_userinfo(loanid,idx)])
#    print(loanid)
    print(i)
    idx += 1
    i += 1 #check how many times of this program loop

table2.to_csv('userinfo2.csv',header=False)

# toc()  #this scarpy use of total time
