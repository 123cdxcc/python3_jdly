#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/1/20 17:08
# @Author : Cdx
# @Site : 
# @File : day_A1.py
# @Software: PyCharm

import requests
import re
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def start(index):
    r=requests.post("https://www.jdlingyu.mobi/", data={'type': 'index', 'paged': index})
    if r.status_code==200:
        html=r.text
        #print(html)
        pic=re.findall(r"http://.{1,80}\.jpg", html)
        print('成功访问第%d页'% index)
        return pic
    else:
        print('第%d页访问失败'% index)
        return [None]
i=0
def dow_start(url,n):
    print("线程%s启动"%threading.current_thread().getName())
    r=requests.get(url, timeout=2.5)
    if r.status_code==200:
        b_image=r.content
        #print(b_image)
        with open('image/_%d_%s'%(n, os.path.split(url)[1]), "wb") as f:
            f.write(b_image)
            global i
            i+=1
            print('下载成功%d'% i)
    else:
        print('连接失败')
sta=time.time()

executor = ThreadPoolExecutor(max_workers=10)

n=1
while n<=100:
    pic=start(n)
    #print('第%d也开始下载'%n)
    time.sleep(0.5)
    for url in pic:
        #dow_start(url)
        executor.submit(dow_start, url,n)
        #threading.Thread(target=dow_start,args=(url,)).start()
    n=n+1
    if n==101:
        end=time.time()
        print("耗时：%d"%(sta-end))

print('运行完毕')