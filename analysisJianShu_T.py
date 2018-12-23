#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib import request
from  bs4 import BeautifulSoup
import re
import time
import sqlite3
from lxml import etree
import json
import datetime
import threading
import queue
#from lxml.etree import HTMLParser


class AnalysisAuthor:
    info=[]
    following_name=[]
    follower_name=[]
    title_href=[]
    url_header="https://www.jianshu.com/"
    def __init__(self,url):
        self.info.clear()
        self.follower_name.clear()
        self.following_name.clear()
        self.title_href.clear()
        self.url_short=url
        self.url=self.url_header+"/u/"+url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(self.url,headers=self.headers)
        #time.sleep(1)
        try:
            self.page_info = request.urlopen(self.page).read().decode('utf-8')
            self.soup = BeautifulSoup(self.page_info, 'html.parser')
        except :
            return
        
    
    def GetName(self):
        self.name=self.soup.find('a','name').string
        #print(self.name)
        return self.name
    
    def GetAuthorInfo(self):
        
        self.following=self.soup.find_all('div','meta-block')
        for self.i in self.following:
            self.info.append(self.i.find('p').string)
        return self.info

    def GetFollowing(self):
        self.page=2
        self.flist=[]
        self.url_following=self.url_header+"users/"+self.url_short+"/following"
        #print(self.url_following)
        self.page_following=request.Request(self.url_following,headers=self.headers)
        #time.sleep(1)
        self.page_info_following=request.urlopen(self.page_following).read().decode('utf-8')
        self.soup_following=BeautifulSoup(self.page_info_following, 'html.parser')
        self.followinginfo=self.soup_following.find_all('a','avatar')
        for self.fi in self.followinginfo:
            #print(self.fi.get('href'))
            self.flist.append((self.fi.get('href')[3:len(self.fi.get('href'))]))
            #print(self.fi.get('href')[3:len(self.fi.get('href'))])
            self.following_name.append(self.fi.get('href')[3:len(self.fi.get('href'))])
        #self.following_name.append(self.flist)
        while(len(self.flist)>9):
            self.flist.clear()
            self.url_following_1=self.url_following+"?page="+str(self.page)
            #print(self.url_following_1)
            self.page_following=request.Request(self.url_following_1,headers=self.headers)
            #time.sleep(1)
            self.page_info_following=request.urlopen(self.page_following).read().decode('utf-8')
            self.soup_following=BeautifulSoup(self.page_info_following, 'html.parser')
            self.followinginfo=self.soup_following.find_all('a','avatar')
            for self.fi in self.followinginfo:
                #print(self.fi.get('href'))
                #print(self.fi.get('href')[3:len(self.fi.get('href'))])
                self.flist.append(self.fi.get('href')[3:len(self.fi.get('href'))])
                self.following_name.append(self.fi.get('href')[3:len(self.fi.get('href'))])
            
            #self.following_name.append(self.flist)
            self.page=self.page+1
            if(self.page>100):
                return self.following_name

        self.num=self.following_name.count(self.url_short)
        for self.temp in range(0,self.num):
            self.following_name.remove(self.url_short)

        return self.following_name
    
    def GetFollower(self):
        self.follower_page=2
        self.fslist=[]
        self.follower_url=self.url_header+"users/"+url+"/followers"
        self.page_follower=request.Request(self.follower_url,headers=self.headers)
        #time.sleep(1)
        self.page_info_follower=request.urlopen(self.page_follower).read().decode('utf-8')
        self.soup_follower=BeautifulSoup(self.page_info_follower, 'html.parser')
        self.followerinfo=self.soup_follower.find_all('a','avatar')
        for self.fsi in self.followerinfo:
            self.fslist.append((self.fsi.get('href')[3:len(self.fsi.get('href'))]))
            self.follower_name.append(self.fsi.get('href')[3:len(self.fsi.get('href'))])
        while(len(self.fslist)>9):
            self.fslist.clear()
            self.url_follower_1=self.follower_url+"?page="+str(self.follower_page)
            print(self.url_follower_1)
            self.page_follower=request.Request(self.url_follower_1,headers=self.headers)
            #time.sleep(1)
            self.page_info_follower=request.urlopen(self.page_follower).read().decode('utf-8')
            self.soup_follower=BeautifulSoup(self.page_info_follower, 'html.parser')
            self.followerinfo=self.soup_follower.find_all('a','avatar')
            for self.fsi in self.followerinfo:
                self.fslist.append((self.fsi.get('href')[3:len(self.fsi.get('href'))]))
                self.follower_name.append(self.fsi.get('href')[3:len(self.fsi.get('href'))])
            
            self.follower_page=self.follower_page+1
            if(self.follower_page>100):
                return self.follower_name
            #time.sleep(3)

        self.num_follower=self.follower_name.count(self.url_short)
        for self.temp in range(0,self.num_follower):
            self.follower_name.remove(self.url_short)
            
        return self.follower_name

    def GetTitle(self):
        self.tilist=[]
        self.t_page_num=2
        self.title=self.soup.find_all('a','title')
        for self.ti in self.title:
            print(self.ti.get('href')[3:len(self.ti.get('href'))])
            self.tilist.append(self.ti.get('href')[3:len(self.ti.get('href'))])
            self.title_href.append(self.ti.get('href')[3:len(self.ti.get('href'))])
        while(len(self.tilist)>8):
            self.tilist.clear()
            self.t_url=self.url_header+"u/"+self.url_short+"?order_by=shared_at&page="+str(self.t_page_num)
            print(self.t_url)
            self.t_page=request.Request(self.t_url,headers=self.headers)
            #time.sleep(1)
            self.page_info_t=request.urlopen(self.t_page).read().decode('utf-8')
            self.soup_t=BeautifulSoup(self.page_info_t,'html.parser')
            self.title=self.soup_t.find_all('a','title')
            for self.ti in self.title:
                print(self.ti.get('href')[3:len(self.ti.get('href'))])
                self.tilist.append(self.ti.get('href')[3:len(self.ti.get('href'))])
                self.title_href.append(self.ti.get('href')[3:len(self.ti.get('href'))])
            if(len(self.tilist)>10):
                return self.title_href
            self.t_page_num=self.t_page_num+1
            if(self.t_page_num>200):
                return self.title_href
        return self.title_href




            #https://www.jianshu.com/u/9ed50acac61c?order_by=shared_at&page=5









class GetTitleinfo:
    url_header="https://www.jianshu.com/"
    
    def __init__(self,url):
        self.url=self.url=self.url_header+"p/"+url
        print(self.url)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(self.url,headers=self.headers)
        try:
            #time.sleep(1)
            self.page_info = request.urlopen(self.page).read().decode('utf-8')
            self.selector=etree.HTML(self.page_info)
            self.test=self.selector.xpath("//script[@type='application/json']")
            self.author_json=json.loads(self.test[0].text)
        except :
            return 
        #time.sleep(1)
        #self.page_info = request.urlopen(self.page).read().decode('utf-8')
        
        #print(self.author_json)

    def Getwordage(self):        
        return self.author_json['note']['public_wordage']
        
    def GetPubilc_time(self):
        self.public_time=self.selector.xpath("//span[@class='publish-time']")
        #print(self.public_time[0].get('title'))
        if(len(self.public_time)<1):
            return 0
        try:
            self.time=self.public_time[0].get('title')[6:len(self.public_time[0].get('title'))]
            self.dt=datetime.datetime.strptime(self.time, "%Y.%m.%d %H:%M")
        except :
            return 0
        
        
        return self.dt

    def GetViewcount(self):       
        return self.author_json['note']['views_count']
    
    def GetLikecount(self):
        return self.author_json['note']['likes_count']
        
    def GetCommondcount(self):
        return self.author_json['note']['comments_count']
    
    def GEtAuthorName(self):
        self.getname=self.selector.xpath("//a[@class='avatar']")
        self.temp=self.getname[0].get('href')
        return self.temp[3:len(self.temp)]
        
       

        
      
class initJianshu:
    def __init__(self):
        self.url="https://www.jianshu.com"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(self.url,headers=self.headers)
        self.page_info = request.urlopen(self.page).read().decode('utf-8')
        self.soup = BeautifulSoup(self.page_info, 'html.parser')
        self.authors=self.soup.find_all('a','nickname')
        for self.author in self.authors:
            #print(self.author.get('href')[3:len(self.author.get('href'))])
            author_list.append(self.author.get('href')[3:len(self.author.get('href'))])
        






#main
db_path='/home/j/python/python/test.db'
conn=sqlite3.connect(db_path)
c=conn.cursor()
author_list=[]
title_list=[]
initJianshu()

threadnum=10
threads=[]
bq=queue.Queue()
def Tgettile(title_url):    
    try:
        t_url=GetTitleinfo(title_url)
        tinfo=[title_url,t_url.GEtAuthorName(),t_url.GetPubilc_time(),t_url.Getwordage(),t_url.GetViewcount(),t_url.GetCommondcount(),t_url.GetLikecount()]
        bq.put(tinfo)
        print("inst ")
        print(tinfo)
        print("to quene")
    except :
        return

def InsterToDB(bq):
    t_db_path='/home/j/python/python/test.db'
    t_conn=sqlite3.connect(t_db_path)
    t_c=t_conn.cursor()
    while(1):
        if(bq.empty()):
            time.sleep(1)
            continue
        temp=bq.get()
        print(temp)
        t_c.execute('INSERT INTO title VALUES (?,?,?,?,?,?,?)',(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6]))
        t_conn.commit()


t_insert=threading.Thread(target=InsterToDB,args=(bq,))
t_insert.start()

#print(len(author_list))
while(len(author_list)>0):
    url=author_list.pop(0)
    #print(type(url))
    print("analysis:"+url+"\n")
    #cursor.execute('select * from user where name=? and pwd=?', ('abc', '123456'))
    c.execute('SELECT * FROM author WHERE url=?',[url])
    result=c.fetchone()
    #print(type(c.fetchall()))
    if(result!=None):
        continue
    a_url=AnalysisAuthor(url)
    #print(a_url.GetName())
    #print(a_url.GetAuthorInfo())
    #print(int(a_url.GetAuthorInfo()[0]))
    try:
        c.execute('INSERT INTO author VALUES (?,?,?,?,?,?,?)',(url,a_url.GetName(),int(a_url.GetAuthorInfo()[0]),int(a_url.GetAuthorInfo()[1]),int(a_url.GetAuthorInfo()[2]),int(a_url.GetAuthorInfo()[3]),int(a_url.GetAuthorInfo()[4])))
        #c.execute('INSERT INTO test1 VALUES (?,?)',(author.string,aaa))
        print("instert"+url+"to DB")
        conn.commit()
    except :
        continue
    
    if(len(author_list)<100):
        author_list.extend(a_url.GetFollower())
        author_list.extend(a_url.GetFollowing())
    
    title_list.extend(a_url.GetTitle())
    while(len(title_list)!=0):
        threads=[]
        if(len(title_list)>10):
            threadnum=10
        if(len(title_list)<10):
            threadnum=len(title_list)
        for i in range(0,threadnum):
            title_url=title_list.pop(0)
            t=threading.Thread(target=Tgettile,args=(title_url,))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    
    #time.sleep(1000)    

        """ title_url=title_list.pop(0)
        t_url=GetTitleinfo(title_url)
        if(t_url==0):
            continue
        try:
            c.execute('INSERT INTO title VALUES (?,?,?,?,?,?,?)',(title_url,t_url.GEtAuthorName(),t_url.GetPubilc_time(),t_url.Getwordage(),t_url.GetViewcount(),t_url.GetCommondcount(),t_url.GetLikecount()))
            print("instert: "+title_url+" to DB")
            conn.commit()
        except :
            continue """
        
        


""" url="74b0e0bfe47a"
aaa=GetTitleinfo(url)
#aaa.qtest()
print(aaa.GetPubilc_time())
print(type(aaa.GetPubilc_time()))
print(aaa.GetViewcount())
print(aaa.GetCommondcount())
print(aaa.GetLikecount())
print(aaa.Getwordage())
print(type(aaa.GetViewcount()))
print(aaa.GEtAuthorName()) """
""" aaa=AnalysisTitle(url)
aaa.GetTitleName()
aaa.GetAuthor()
aaa.GetPubilc_time()
aaa.GetWordage() """
#aaa=AnalysisAuthor(url)
#aaa.GetTitle()
#print(len(aaa.GetTitle()))

#aaa=AnalysisTitle(url)
#aaa.GetTitleHref()

""" 
aaa=AnalysisAuthor(url)
b=aaa.GetFollower()
for i in range(0,len(b)):
    print(b[i]) """
#aaa=AnalysisAuthor(url)
#b=aaa.GetName()
#print(b)
#aaa.GetAuthorInfo()
#c=aaa.GetAuthorInfo()
#print(c)
#aaa.GetFollowing()

#print(len(aaa.GetFollowing()))
#print(len(list(set(aaa.GetFollowing()))))