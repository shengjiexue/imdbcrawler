#-*- coding:utf-8 -*-
'''
该段代码定义了若干getInfoOfOneMovie.py中用到的函数
前面6个函数都在第7个函数也就是appendOne中调用
'''
import lxml.html
import time
from pandas import DataFrame
import urllib2
import pandas as pd
import re
import random

# 得到网页的xml格式数据内容


def getDoc(url_oneMovie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    request = urllib2.Request(url_oneMovie, headers=headers)  # 发送请求
    response = urllib2.urlopen(request)  # 获得响应
    time.sleep(1 + random())
    content = response.read()  # 获取网页内容
    doc = lxml.html.fromstring(content)  # 可能是将网页以xml格式解析
    return doc

# 通过xml数据得到导演信息


def getDirectors(doc, url_oneMovie):
    directors = doc.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    for i in range(len(directors)):
        directors[i] = unicode(directors[i]).encode('utf-8')
    return directors  # 返回的是list

# 通过xml数据得到主演信息


def getLeadingRoles(doc, url_oneMovie):
    leadingRoles = doc.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
    # 有些有些豆瓣电影信息里没有编剧这一项，所以主演会在第二条信息里。
    # 所以需要判断得到的主演列表是否为空
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    if leadingRoles == []:
        leadingRoles = doc.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
    for i in range(len(leadingRoles)):
        leadingRoles[i] = unicode(leadingRoles[i]).encode('utf-8')
    return leadingRoles  # 返回的是list

# 通过xml数据得到上映日期信息


def getReleaseDate(doc, url_oneMovie):
    releaseDate = doc.xpath('//*[@id="info"]/span/text()')  # 得到的是一个list，其中有一个元素是上映日期
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    for i in range(len(releaseDate)):
        releaseDate[i] = unicode(releaseDate[i]).encode('utf-8')
    temp = re.compile(r'\d*-\d*-\d*')
    for i in range(len(releaseDate)):
        if re.findall(temp, releaseDate[i]) != []:  # findall返回的是能匹配到的list，所以用是否为[]进行判断
            return releaseDate[i]  # 返回的是str

# 通过xml数据得到又名信息


def getAlterNames(doc, url_oneMovie):
    tempList = doc.xpath('//*[@id="info"]/text()')  # 得到的是一个list，最后一个非空的元素就是又名
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    for i in range(len(tempList)):
        tempList[i] = unicode(tempList[i]).encode('utf-8')
    # 取出‘又名’的名字字符串
    temp = re.compile(r'\S')  # 匹配非空字符串的正则表达式
    for i in range(len(tempList)):  # 取出非空字符串，最后一个才是‘又名’
        if re.findall(temp, tempList[i]) != []:  # 如果匹配的结果非空
            alterNames = tempList[i]  # 由于不停的循环，找到的最后一个非空的字符串才是’又名‘
    return alterNames  # 返回‘又名’,格式为str

# 通过xml数据得到IMDB链接信息


def getIMDBurl(doc, url_oneMovie):
    xpathList = doc.xpath('//*[@id="info"]/a/text()')
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    # 有些豆瓣电影没有对应的IMDB网址，所以要判断一下是否为[]
    if xpathList != []:
        for i in range(len(xpathList)):
            xpathList[i] = unicode(xpathList[i]).encode('utf-8')
        # 取出通过//*[@id="info"]/a得到的形如‘tt12345678’的IMDBurl的ID
        # 有三种情况：
        # 1、xpathList长度为1，第一项为tt12345678
        # 2、xpathList长度为1，第一项为豆瓣内容专题
        # 3、xpathList长度为2，第二项为tt12345678
        # 此处采用正则表达式
        temp = re.compile(r'tt\d{3,}')
        for i in range(len(xpathList)):
            tempList = re.findall(temp, xpathList[i])
            if tempList != []:
                IMDBurlID = tempList[0]  # 得到形如‘tt12345678’的IMDBurl的ID或者None
        IMDBurl = 'http://www.imdb.com/title/' + IMDBurlID + '/'  # 将ID转换成IMDB网址
        return IMDBurl  # 返回IMDB网址
    else:
        return '-'


def getIMDBID(doc, url_oneMovie):
    xpathList = doc.xpath('//*[@id="info"]/a/text()')
    # 将列表中的每一项先转换成unicode，再转换成utf-8格式
    # 有些豆瓣电影没有对应的IMDB网址，所以要判断一下是否为[]
    if xpathList != []:
        for i in range(len(xpathList)):
            xpathList[i] = unicode(xpathList[i]).encode('utf-8')
        # 取出通过//*[@id="info"]/a得到的形如‘tt12345678’的IMDBurl的ID
        # 有三种情况：
        # 1、xpathList长度为1，第一项为tt12345678
        # 2、xpathList长度为1，第一项为豆瓣内容专题
        # 3、xpathList长度为2，第二项为tt12345678
        # 此处采用正则表达式
        temp = re.compile(r'tt\d{3,}')
        for i in range(len(xpathList)):
            tempList = re.findall(temp, xpathList[i])
            if tempList != []:
                IMDBurlID = tempList[0]  # 得到形如‘tt12345678’的IMDBurl的ID或者None
        return IMDBurlID  # 返回IMDBID
    else:
        return '-'


def appendOne(movieInfo, url_oneMovie):
    doc = getDoc(url_oneMovie)
    directors = getDirectors(doc, url_oneMovie)  # 得到的是若干导演的一个list
    leadingRoles = getLeadingRoles(doc, url_oneMovie)  # 得到的是若干主演的一个list
    releaseDate = getReleaseDate(doc, url_oneMovie)  # 得到的是str字符串
    alterNames = getAlterNames(doc, url_oneMovie)  # 得到的是str字符串
    IMDBurl = getIMDBurl(doc, url_oneMovie)  # 得到的str格式的IMDB网址
    # IMDBID = getIMDBID(doc, url_oneMovie) # get IMDBID
    tempDf = DataFrame({'directors': [directors], 'leadingRoles': [leadingRoles], 'releaseDate': [
                       releaseDate], 'alterNames': [alterNames], 'IMDBurl': [IMDBurl]})
    movieInfo = pd.concat([movieInfo, tempDf])
    return movieInfo
