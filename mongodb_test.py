#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pymongo import MongoClient

myclient =MongoClient("mongodb://localhost:27017/")
dblists = myclient.test
# dblist = myclient.database_names() 
my_set=dblists.admin
url='eda90c174661'
a=my_set.find({'url':url})
b=my_set.find({'url':'eda90c174661'})
print(a.count())
for i in a:
    print(i['name'])