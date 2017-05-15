# -*- coding: utf-8 -*-
'''
该段代码可以通过step3_getInfoOfOneMovie.py得到的
doubanMovies_scoreInfoAdded.csv文件中的IMDBurl
定位到每个豆瓣电影对应的IMDB链接
然后解析IMDB链接的内容，得到每个电影在IMDB上的IMDBRate评分
和numOfPeopleWhoRate打分人数
'''
import requests    #此处采用requests方法得到网页响应
import json
import time
from pandas import DataFrame
import pandas as pd
import urllib2
import time
import lxml.html
from pandas import DataFrame
doubanMovie_info=pd.read_csv('doubanMovies_scoreInfoAdded.csv')    #取出数据结构为DataFrame的doubanMovies_info
IMDBurl=doubanMovie_info['IMDBurl']    #IMDBurl为一个Series
IMDBRateList=[]    #初始化IMDBRateList，就是所有的IMDB评分的一个列表
numOfPeopleWhoRateList=[]

#函数： 获取IMDB的json数据
def getIMDBjson(id):
	data_oneTag=[]
	headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
	url='http://www.omdbapi.com/?i=tt'+str(id)+'&'
	resp=requests.get(url,headers=headers)
	data_oneSubject=json.loads(resp.text)
	#print data_oneSubject
	time.sleep(1)    
	return data_oneSubject


	#data_allTag+=data_oneTag    #将每个标签下的得到的数据加入到data_allTag数据集中，最终的data_allTag为数据list数据结构，每一项为一个字典
	#moviesNum+=len(data_oneTag)     #计算所有标签下电影的总数（包含重复项）
	#print tag+':',len(data_oneTag)    #打印出各个标签下得到的电影数

#print '电影总数为:',moviesNum #打印出总电影数，该数字没有消除重复项
#for i in range(5):
#    print data_allTag[i]['title']+' '+data_allTag[i]['rate']    #打印出data_allTag的前10项，只输出键'title'和'rate'对应的值

#df=DataFrame(data_allTag)

#title列为unicode编码格式，在将数据输出为csv格式时会出现编码问题，所以下面三行将title列数据转换为utf-8格式
#title=df['title']
#title=title.map(lambda x:x.encode('utf-8'))
#df['title']=title

#将结果中rate列的数字转换为float格式
#rate=df['rate']   #将df的rate列取出，格式为Series
#rate=rate.map(float)    #将rate列中的数值转换为float格式
#df['rate']=rate    #将df中的rate列替换为float格式的rate列

#将DataFrame格式的结果数据写入csv格式的文件中
#df.to_csv('doubanMovies.csv',index=False,header=True)

# #将数据结构为list的data_allTag转换成json格式后保存到doubanMovie.js文件中
# try:
#     f1=open('doubanMovies.js','w')
#     f1.write(json.dumps(data_allTag))    #将list数据结构的data_allTag写入json文件
# except:
#     print '写入js文件未成功！'
# finally:
#     f1.close()    #注意关闭文件流
data_allTag=[]
for i in range(0,len(IMDBurl)):
    print i+1    #打印出当前位置，作为标记
    if IMDBurl[i]!='-':    #如果有IMDB链接
    	data_oneTag=getIMDBjson(IMDBurl[i][28:35])
    	data_allTag.append(data_oneTag)
    	print data_oneTag
    else:
		print 'Movie:',i+1,'Without IMDBurl,No.'

#print data_allTag
print len(data_allTag)
df=DataFrame(data_allTag)
df.to_csv('imdbMovies.csv',index=False,header=True)
