#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from urllib import request
from  bs4 import BeautifulSoup
import re
import time
import sqlite3

#author_list待爬取的列表 
author_list=[]

#链接数据库
db_path='/home/j/code/python/python/test.db'
conn=sqlite3.connect(db_path)
c=conn.cursor()

class analysisURL:
    def __init__(self,url):
        self.url=url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(url,headers=self.headers)
        self.page_info = request.urlopen(self.page).read().decode('utf-8')
        self.soup = BeautifulSoup(self.page_info, 'html.parser')
        

    def get_info(self):
        following_num=self.soup.find_all('div','info').title
        print(following_num)
        ii=self.soup.find_all('a','href')
        print(ii)



url="https://www.jianshu.com"



# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
#soup = BeautifulSoup(page_info, 'html.parser')
# 以格式化的形式打印html
#print(soup.prettify())
 
#titles = soup.find_all('a', 'title')# 查找所有a标签中class='title'的语句
#authors=soup.find_all('a','nickname') #获取本页中的所有作者
#for title in titles:
#    print(title.string+"\n")
 #   print("http://www.jianshu.com" + title.get('href')+"\n\n")

#for author in authors:
#    print(author.string+"\n") 
    #print("http://www.jianshu.com" + author.get('href')+"\n\n")
#    aaa=author.get('href')
    #c.execute('INSERT INTO test1 VALUES (?,?)',(author.string,aaa))
 #   author_list.append(aaa)

#conn.commit()


#url_pop=author_list.pop(0)
#print(url_pop)
#url_analysis="http://www.jianshu.com" +url_pop

ANAURL=analysisURL('https://www.jianshu.com/u/08fab6d5eca0')
ANAURL.get_info()




