#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pymongo import MongoClient

myclient =MongoClient("mongodb://localhost:27017/")
dblists = myclient.test
# dblist = myclient.database_names() 
my_set=dblists.admin
my_set.insert({"name":"将","age":18})
for i in my_set.find():
    print(i)