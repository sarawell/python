import random
import queue
from urllib import request
from urllib import error
import threading
import sqlite3
import json
from lxml import etree







user_agent_pools=[
         'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
         'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0', 
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
         'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25',
     ]

class InitJianshu:
    def __init__(self):
        init_author=[]
        self.url="https://www.jianshu.com/recommendations/users?utm_source=desktop&utm_medium=index-users"
        self.UA_num=random.choice(user_agent_pools)
        self.headers = {'User-Agent':self.UA_num}
        self.page = request.Request(self.url,headers=self.headers)
        try:
            self.page_info = request.urlopen(self.page)
            if(self.page_info.code==200):
                self.page_text=self.page_info.read().decode('utf-8')
                self.selector=etree.HTML(self.page_text)
                print(type(self.selector))
                self.initinfo_a=self.selector.xpath("//div[@class='wrap']/a/@href")
                
                #print(self.name)
        except error.HTTPError as e:
            print("init Jianshu Failed")
            print("the error code is "+str(self.page_info.code))
            print(e.value)




InitJianshu()
