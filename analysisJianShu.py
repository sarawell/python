#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib import request
from  bs4 import BeautifulSoup
import re
import time
import sqlite3


class AnalysisAuthor:
    info=[]
    following_name=[]
    follower_name=[]
    url_header="https://www.jianshu.com/"
    def __init__(self,url):
        self.url=self.url_header+"/u/"+url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(self.url,headers=self.headers)
        self.page_info = request.urlopen(self.page).read().decode('utf-8')
        self.soup = BeautifulSoup(self.page_info, 'html.parser')
    
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
        self.url_following=self.url_header+"users/"+url+"/following"
        #print(self.url_following)
        self.page_following=request.Request(self.url_following,headers=self.headers)
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

        self.num=self.following_name.count(url)
        for self.temp in range(0,self.num):
            self.following_name.remove(url)

        return self.following_name
    
    def GetFollower(self):
        self.follower_page=2
        self.fslist=[]
        self.follower_url=self.url_header+"users/"+url+"/followers"
        self.page_follower=request.Request(self.follower_url,headers=self.headers)
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
            self.page_info_follower=request.urlopen(self.page_follower).read().decode('utf-8')
            self.soup_follower=BeautifulSoup(self.page_info_follower, 'html.parser')
            self.followerinfo=self.soup_follower.find_all('a','avatar')
            for self.fsi in self.followerinfo:
                self.fslist.append((self.fsi.get('href')[3:len(self.fsi.get('href'))]))
                self.follower_name.append(self.fsi.get('href')[3:len(self.fsi.get('href'))])
            
            self.follower_page=self.follower_page+1
            time.sleep(3)

        self.num_follower=self.follower_name.count(url)
        for self.temp in range(0,self.num_follower):
            self.follower_name.remove(url)
            
        return self.follower_name

    #def GetTitle(self):


class AnalysisTitle:
    url_header="https://www.jianshu.com/"
    def __init__(self,url):
        #self.url=url
        self.url=self.url_header+"/u/"+url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.page = request.Request(self.url,headers=self.headers)
        self.page_info = request.urlopen(self.page).read().decode('utf-8')
        self.soup = BeautifulSoup(self.page_info, 'html.parser')

    def GetTitleHref(self):
        self.titlehref=self.soup.find_all('a','title')
        for self.i in self.titlehref:
            print(self.i.get('href')[3:len(self.i.get('href'))])
        while()

    









url="9ed50acac61c"

aaa=AnalysisTitle(url)
aaa.GetTitleHref()

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