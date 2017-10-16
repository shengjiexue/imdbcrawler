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
import random as rand

doubanMovie_info=pd.read_csv('IMDBallusers.csv')    #取出数据结构为DataFrame的doubanMovies_info
IMDBurl=doubanMovie_info['IMDBRate']    #IMDBurl为一个Series

IMDBRateList=[]    #初始化IMDBRateList，就是所有的IMDB评分的一个列表


def getDoc(url):
	url
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
	request = urllib2.Request('http://www.imdb.com'+url+'comments', headers=headers)  # 发送请求
	response = urllib2.urlopen(request)  # 获得响应
	time.sleep(0.2 + 0.2 * rand.random())
	content = response.read()  # 获取网页内容
	doc = lxml.html.fromstring(content)  # 可能是将网页以xml格式解析
	return doc

#函数：获得IMDB评分
def getIMDBRate(doc,oneIMDBurl):
    #匹配IMDB评分的xpath路径
    temp=[]
    if doc.xpath('//*[@valign="top"]/td/div[1]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[1]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[2]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[2]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[3]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[3]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[4]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[4]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[5]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[5]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[6]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[6]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[7]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[7]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[8]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[8]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[9]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[9]/a/@href')[0])
    if doc.xpath('//*[@valign="top"]/td/div[10]/a/@href'):
    	temp.append(doc.xpath('//*[@valign="top"]/td/div[10]/a/@href')[0])
    #print temp
    #/div[1]/div[3]/div[1]/div[1]/div[2]')
    return temp  #返回的是string格式的数据

#函数：将类似于'123,456'的字符串转换为int数据类型123456
#因为得到的评分人数的格式为'123,456'

num=1   #没有IMDB链接的电影个数，用作统计
startPoint=1 #为了在出错时，从错误的地方重新开始运行，设置了该错误点参数
for i in range(startPoint-1,len(IMDBurl)):
    print i+1    #打印出当前位置，作为标记
    try:
        #由于有些电影没有IMDB链接，所以要进行判断
        if IMDBurl[i]!='-':    #如果有IMDB链接
            doc=getDoc(IMDBurl[i])    #得到xml格式数据
            #print doc
            #得到IMDB评分
            IMDBRate=getIMDBRate(doc,IMDBurl[i])
            for j in range(len(IMDBRate)):
            	IMDBRateList.append(IMDBRate[j])    #将得到的IMDB评分加入IMDBRateList中
            #得到评分人数
            #name=getNumOfPeopleWhoRate(doc,IMDBurl[i])
           
        else:    #如果没有IMDB链接，将两个list列表中都加入'-'表示没有值
            print 'Movie:',i+1,'Without IMDBurl,No.',num  #打印出没有IMDB链接的电影相关信息
            num=num+1    #没有IMDB链接的电影数加1
    except:    #发生未知错误时，将两个list列表中加入'unknownError'，表示出现未知错误
        print 'unknownError happened!'
        #IMDBRateList.append('unknownError')
        #nameList.append('unknownError')
    finally:
        #将两个list列表转换成DataFrame格式，方便往csv格式文件中添加
        IMDBRate=DataFrame({'IMDBRate':IMDBRateList})   #将IMDBRateList转换为DataFrame格式，方便加入其他数据中
        #将DataFrame格式的结果添加到csv格式文件中
        IMDBRate.to_csv('IMDBfinal2.csv',index=False,encoding='utf-8')


        movies_unique = IMDBRate.drop_duplicates()
        movies_unique.to_csv('IMDBtitles.csv', index=False, header=True)