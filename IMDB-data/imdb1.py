# -*- coding: utf-8 -*-
'''
该段代码可以通过step3_getInfoOfOneMovie.py得到的
doubanMovies_scoreInfoAdded.csv文件中的IMDBurl
定位到每个豆瓣电影对应的IMDB链接
然后解析IMDB链接的内容，得到每个电影在IMDB上的IMDBRate评分
和numOfPeopleWhoRate打分人数
'''
import requests  # 此处采用requests方法得到网页响应
import json
import time
from pandas import DataFrame
import pandas as pd
import urllib2
import time
import lxml.html
from pandas import DataFrame
import random as rand
from getAwardScores import *


# 取出数据结构为DataFrame的doubanMovies_info
doubanMovie_info = pd.read_csv('doubanMovies_scoreInfoAdded1.csv')
IMDBurl = doubanMovie_info['IMDBurl']  # IMDBurl为一个Series
IMDBRateList = []  # 初始化IMDBRateList，就是所有的IMDB评分的一个列表
numOfPeopleWhoRateList = []

# 函数： 获取IMDB的json数据


def getIMDBjson(id):
    data_oneTag = []
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    url = 'http://www.omdbapi.com/?i=tt' + str(id) + '&'
    resp = requests.get(url, headers=headers)
    data_oneSubject = json.loads(resp.text)
    # print data_oneSubject
    time.sleep(1 + rand.random())
    return data_oneSubject

data_allTag = []
for i in range(0, 500):
    print i + 1  # 打印出当前位置，作为标记
    if IMDBurl[i] != '-':  # 如果有IMDB链接
        data_oneTag = getIMDBjson(IMDBurl[i][28:35])

        # split Ratings and append them
        if 'Ratings' in data_oneTag.keys():
            data_Rating = data_oneTag['Ratings']
            for i in range(0, len(data_Rating)):
                data_oneTag[data_Rating[i]['Source']] = data_Rating[i]['Value']
        else:
            data_oneTag['Internet Movie Database'] = None
            data_oneTag['Rotten Tomatoes'] = None
            data_oneTag['Metacritic'] = None

        del data_oneTag['Ratings']

        # resolve Awards and append them
        data_Awards = data_oneTag['Awards']

        data_oneTag['Oscar wins'] = get_oscars_wins(data_Awards)
        data_oneTag['Oscar nominations'] = get_oscars_nominations(data_Awards)
        data_oneTag['Golden Globe wins'] = get_golden_wins(data_Awards)
        data_oneTag['Golden Globe nominations'] = get_golden_nominations(data_Awards)
        data_oneTag['other wins'] = get_wins(data_Awards)
        data_oneTag['ohter nominations'] = get_nominations(data_Awards)

        print data_oneTag
        data_allTag.append(data_oneTag)
    else:
        print 'Movie:', i + 1, 'Without IMDBurl,No.'

# print data_allTag
print len(data_allTag)
df = DataFrame(data_allTag)
df.to_csv('imdbMovies.csv', index=False, header=True, encoding='utf8')
