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

#开始的页数
sta_index=0
#结束的页数
end_index=100


#查询页数连接方法，传入页数
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

#下载图片方法，传入连接和页数，图片命名格式为(_页数_图片本身名字.jpg)
i=0
def dow_start(url,n):
    print("线程%s启动"%threading.current_thread().getName())
    r=requests.get(url, timeout=2.5)
    if r.status_code==200:
        b_image=r.content
        with open('image/_%d_%s'%(n, os.path.split(url)[1]), "wb") as f:
            f.write(b_image)
            global i
            i+=1
            print('下载成功%d'% i)
    else:
        print('连接失败')
sta=time.time()

executor = ThreadPoolExecutor(max_workers=10)

while sta_index<=end_index:
    pic=start(sta_index)
    time.sleep(0.5)
    for url in pic:
        executor.submit(dow_start, url, sta_index)
    n=n+1

print('运行完毕')