# -*- coding: utf-8 -*-
'''
该段代码可以通过step3_getInfoOfOneMovie.py得到的
doubanMovies_scoreInfoAdded.csv文件中的IMDBurl
定位到每个豆瓣电影对应的IMDB链接
然后解析IMDB链接的内容，得到每个电影在IMDB上的IMDBRate评分
和numOfPeopleWhoRate打分人数
'''
import pandas as pd
import urllib2
import time
import lxml.html
from pandas import DataFrame
# 取出数据结构为DataFrame的doubanMovies_info
doubanMovie_info = pd.read_csv('doubanMovies_scoreInfoAdded.csv')
IMDBurl = doubanMovie_info['IMDBurl']  # IMDBurl为一个Series
IMDBRateList = []  # 初始化IMDBRateList，就是所有的IMDB评分的一个列表
numOfPeopleWhoRateList = []


def getDoc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    request = urllib2.Request(url, headers=headers)  # 发送请求
    response = urllib2.urlopen(request)  # 获得响应
    time.sleep(1)
    content = response.read()  # 获取网页内容
    doc = lxml.html.fromstring(content)  # 可能是将网页以xml格式解析
    return doc

# 函数：获得IMDB评分


def getIMDBRate(doc, oneIMDBurl):
    # 匹配IMDB评分的xpath路径
    tempList = doc.xpath(
        '//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
    return float(tempList[0])  # 返回的是float格式的数据

# 函数：将类似于'123,456'的字符串转换为int数据类型123456
# 因为得到的评分人数的格式为'123,456'


def toInt(numWithDot):
    temp1 = numWithDot.split(',')  # 首先将字符串以‘,’分割成list
    temp2 = ''  # 初始化一个字符串
    for i in range(len(temp1)):  # 通过循环，将temp1中的各个元素项合并成一个字符串
        temp2 += temp1[i]
    temp2 = int(temp2)  # 将合并后的数字字符串转换成int格式
    return temp2

# 函数：得到评分人数


def getNumOfPeopleWhoRate(doc, oneIMDBurl):
    # 匹配评分人数的xpath路径
    tempList = doc.xpath(
        '//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/a/span/text()')
    temp = str(tempList[0])  # 得到人数，此时为str数据类型
    numOfPeopleWhoRate = toInt(temp)  # 用前面定义的函数转换数据为int类型
    return numOfPeopleWhoRate  # 返回int类型的评分人数

num = 1  # 没有IMDB链接的电影个数，用作统计
startPoint = 1  # 为了在出错时，从错误的地方重新开始运行，设置了该错误点参数
for i in range(startPoint - 1, len(IMDBurl)):
    print i + 1  # 打印出当前位置，作为标记
    try:
        # 由于有些电影没有IMDB链接，所以要进行判断
        if IMDBurl[i] != '-':  # 如果有IMDB链接
            doc = getDoc(IMDBurl[i])  # 得到xml格式数据
            # 得到IMDB评分
            IMDBRate = getIMDBRate(doc, IMDBurl[i])
            IMDBRateList.append(IMDBRate)  # 将得到的IMDB评分加入IMDBRateList中
            # 得到评分人数
            numOfPeopleWhoRate = getNumOfPeopleWhoRate(doc, IMDBurl[i])
            numOfPeopleWhoRateList.append(numOfPeopleWhoRate)  # 将评分人数加入列表
        else:  # 如果没有IMDB链接，将两个list列表中都加入'-'表示没有值
            print 'Movie:', i + 1, 'Without IMDBurl,No.', num  # 打印出没有IMDB链接的电影相关信息
            num = num + 1  # 没有IMDB链接的电影数加1
            IMDBRateList.append('-')
            numOfPeopleWhoRateList.append('-')
    except:  # 发生未知错误时，将两个list列表中加入'unknownError'，表示出现未知错误
        print 'unknownError happened!'
        IMDBRateList.append('unknownError')
        numOfPeopleWhoRateList.append('unknownError')
    finally:
        # 将两个list列表转换成DataFrame格式，方便往csv格式文件中添加
        # 将IMDBRateList转换为DataFrame格式，方便加入其他数据中
        IMDBRate = DataFrame(
            {'IMDBRate': IMDBRateList, 'numOfPeopleWhoRate': numOfPeopleWhoRateList})
        # 将DataFrame格式的结果添加到csv格式文件中
        IMDBRate.to_csv('IMDBRate.csv', index=False, encoding='utf-8')
