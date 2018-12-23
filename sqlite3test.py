from urllib import request
from  bs4 import BeautifulSoup
import re
import time
import sqlite3
from lxml import etree
import json
import datetime

db_path='/home/j/python/python/test.db'
url='4ac7245baef1'
conn=sqlite3.connect(db_path)
c=conn.cursor()
c.execute('SELECT * FROM author WHERE url=?',[url])
result=c.fetchone()
#if(len(result))
if(result==None):
    print(111)
print(len(result))
print(result)

#print(result.rowcount)
for i in result:
    print(i)
print(url)