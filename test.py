#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from urllib import request
from  bs4 import BeautifulSoup
import re
import time

url="https://www.jianshu.com"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url,headers=headers)
page_info = request.urlopen(page).read().decode('utf-8')


# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
soup = BeautifulSoup(page_info, 'html.parser')
# 以格式化的形式打印html
#print(soup.prettify())
 
titles = soup.find_all('a', 'title')# 查找所有a标签中class='title'的语句
authors=soup.find_all('a','nickname') #获取本页中的所有作者
for title in titles:
    print(title.string+"\n")
    print("http://www.jianshu.com" + title.get('href')+"\n\n")

for author in authors:
    print(author.string+"\n") 
    print("http://www.jianshu.com" + author.get('href')+"\n\n")
