import random
import queue
from urllib import request
from urllib import error
from  bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import threading


errorText="/home/j/python/python/error.txt"


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

author_queue=[]
insert_queue=queue.Queue()

insertstring={"name":"","url":"","following":"","follower":"","title":"","wordages":"","likecount":""}

threadNum=10
threads=[]


class initJianshu:
    def __init__(self):
        self.url="https://www.jianshu.com"
        self.UA_num=random.choice(user_agent_pools)
        self.headers = {'User-Agent':self.UA_num}
        self.page = request.Request(self.url,headers=self.headers)
        try:
            self.page_info = request.urlopen(self.page)
            if(self.page_info.code==200):
                self.page_text=self.page_info.read().decode('utf-8')
                self.soup = BeautifulSoup(self.page_text, 'html.parser')
                self.authors=self.soup.find_all('a','nickname')
                for self.author in self.authors:
                    print(self.author.get('href')[3:len(self.author.get('href'))])
                    author_queue.append(self.author.get('href')[3:len(self.author.get('href'))])
                #author_list.append(self.author.get('href')[3:len(self.author.get('href'))])

        except error.HTTPError as e:
            print("init failed\n"+e.value)
        
class initPage:
    def __init__(self,url):
        self.url=url
    def getpage_text(self):
        self.UA_num=random.choice(user_agent_pools)
        self.headers = {'User-Agent':self.UA_num}
        self.page = request.Request(self.url,headers=self.headers)
        #time.sleep(1)
        try:
            self.page_info = request.urlopen(self.page)
            #time.sleep(1)
            if(self.page_info.code==200):
                self.page_text=self.page_info.read().decode('utf-8')
                #time.sleep(1)
                self.soup = BeautifulSoup(self.page_text, 'html.parser')
                #time.sleep(1)
                return self.soup
        except error.HTTPError as e:
            print(e.code)
            return 0

class AnalysisAuthor:
    following_list=[]
    follower_list=[]
    title_list=[]
    def __init__(self,url):
        self.url=url
        self.a_url_full='https://www.jianshu.com/u/'+self.url
        self.a_initpage=initPage(self.a_url_full)
        self.a_getpage_text=self.a_initpage.getpage_text()
        
    def GetInfo(self):
        if self.a_getpage_text!=None:
            self.a_author_name=self.a_getpage_text.find('a','name').string
            print('author_name: '+self.a_author_name)
            self.a_author_info=self.a_getpage_text.find_all('div','meta-block')
            self.a_author_following=int(self.a_author_info[0].find('p').string)
            print('author_following: '+str(self.a_author_following))
            self.a_author_follower=int(self.a_author_info[1].find('p').string)
            print('author_follower: '+str(self.a_author_follower))
            self.a_author_title=int(self.a_author_info[2].find('p').string)
            print('author_title: '+str(self.a_author_title))
            self.a_author_wordages=int(self.a_author_info[3].find('p').string)
            print('author_wordages: '+str(self.a_author_wordages))
            self.a_author_likescount=int(self.a_author_info[4].find('p').string)
            print('author_likescount: '+str(self.a_author_likescount))
        else:
            return None

    def GetFollowing(self):
        self.following_list.clear()
        self.following_page_num=1
        self.following_page_count=int(self.a_author_following)/9+1
        if(int(self.a_author_following)>0):
            while(len(self.following_list)<int(self.a_author_following)):
                self.following_url_header='https://www.jianshu.com/users/'+self.url+'/following'+"?page="+str(self.following_page_num)
                print(self.following_url_header)
                self.following_page=initPage(self.following_url_header)
                self.following_page_text=self.following_page.getpage_text()
                if(self.following_page_text!=None):
                    self.follow_info=self.following_page_text.find_all('a','avatar')
                    for self.fwing in self.follow_info:
                        self.temp=self.fwing.get('href')[3:len(self.fwing.get('href'))]
                        if(self.temp!=self.url):
                            if(self.following_list.count(self.temp)==0):
                                self.following_list.append(self.temp)
                                if(len(author_queue)<20):
                                    author_queue.append(self.temp)
                            else:
                                pass

                else:
                    pass
                self.following_page_num=self.following_page_num+1
                if(self.following_page_num>self.following_page_count):
                    return self.following_list
            """ while(len(self.following_list)<int(self.a_author_following))):
                self.following_page_num=self.following_page_num+1
                self.following_url_header='https://www.jianshu.com/users/'+self.url+'/following'+"?page="+str(self.following_page_num)
                print(self.following_url_header)
                self.following_page=initPage(self.following_url_header)
                self.following_page_text=self.following_page.getpage_text() """
        else:
            return self.following_list
        return self.following_list

    def GetFollower(self):
        self.follower_list.clear()
        self.follower_page_num=1
        self.follower_page_count=int(self.a_author_follower)/9+1
        if(int(self.a_author_follower)>0):
            while(len(self.follower_list)<int(self.a_author_follower)-1):
                self.follower_url_header='https://www.jianshu.com/users/'+self.url+'/followers'+"?page="+str(self.follower_page_num)
                print(self.follower_url_header)
                self.follower_page=initPage(self.follower_url_header)
                self.follower_page_text=self.follower_page.getpage_text()
                if (self.follower_page_text!=None):
                    self.follower_info=self.follower_page_text.find_all('a','avatar')
                    for self.fwer in self.follower_info:
                        self.fwer_temp=self.fwer.get('href')[3:len(self.fwer.get('href'))]
                        if(self.fwer_temp!=self.url):
                            if(self.follower_list.count(self.fwer_temp)==0):
                                self.follower_list.append(self.fwer_temp)
                                if(len(author_queue)<20):
                                    author_queue.append(self.fwer_temp)
                            
                self.follower_page_num=self.follower_page_num+1
                if(self.follower_page_num>self.follower_page_count):
                    return self.follower_list
        else:
            return self.follower_list
        
        return self.follower_list


    
    def GetTitles(self):
        self.title_page_num=1
        self.temp_count=self.a_author_title
        if(int(self.a_author_title)>0):
            while(self.temp_count>0):
                self.title_url_header='https://www.jianshu.com/u/'+self.url+'?order_by=shared_at&page='+str(self.title_page_num)
                print(self.title_url_header)
                self.title_page=initPage(self.title_url_header)
                self.title_page_text=self.title_page.getpage_text()
                if(self.title_page_text!=None):
                    self.title_info=self.title_page_text.find_all('a','title')
                    for self.ti in self.title_info:
                        self.title_temp=self.ti.get('href')[3:len(self.ti.get('href'))]
                        if(self.title_list.count(self.title_temp)==0):
                            self.title_list.append(self.title_temp)
                            print(self.title_temp)
                    self.temp_count=self.temp_count-9
                    self.title_page_num=self.title_page_num+1
                else:
                    self.title_page_num=self.title_page_num-1
                    continue
                

        else:
            return None
        
    
""" def GetAuthor(url):
    try:
        insertstring={"name":"","url":"","following":"","follower":"","title":"","wordages":"","likecount":""}
        a=AnalysisAuthor(url)
        a.GetInfo()
        insertstring['name']=a.a_author_name
        insertstring['url']=url
        followerlist=a.GetFollower()
        insertstring['follower']={'count':a.a_author_follower,'detal':followerlist}
        followinglist=a.GetFollowing()
        insertstring['following']={'count':a.a_author_following,'detal':followinglist}
        insertstring['title']=a.a_author_title
        insertstring['wordages']=a.a_author_wordages
        insertstring['likecount']=a.a_author_likescount
        return insertstring
        #insert_queue.put(insertstring)
    except :
        return None """


def insertDB(insert_queue):
    myclient =MongoClient("mongodb://localhost:27017/")
    dblists = myclient.test
    my_set=dblists.admin
    while(1):
        if(insert_queue.empty()):
            time.sleep(10)
            continue
        temp=insert_queue.get()
        my_set.insert(temp)
        print("insert: "+temp['name']+"to moangodb")
        time.sleep(1)


#initJianshu()
url='db8c0c1c4c99'
insertstring={"name":"","url":"","following":"","follower":"","title":"","wordages":"","likecount":""}
a=AnalysisAuthor(url)
a.GetInfo()
insertstring['name']=a.a_author_name
insertstring['url']=url
followerlist=a.GetFollower()
insertstring['follower']={'count':a.a_author_follower,'detal':followerlist}
followinglist=a.GetFollowing()
insertstring['following']={'count':a.a_author_following,'detal':followinglist}
insertstring['title']=a.a_author_title
insertstring['wordages']=a.a_author_wordages
insertstring['likecount']=a.a_author_likescount


