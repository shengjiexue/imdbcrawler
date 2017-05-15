# -*- coding: utf-8 -*-
'''
该脚本利用step1_doubanMovies.py脚本中得到的csv格式文件进行处理
对豆瓣电影进行了去重
并由rate列得到了score列
'''
import pandas as pd
df=pd.read_csv('doubanMovies.csv')
movies_unique=df.drop_duplicates()    #去重
movies_unique.to_csv('doubanMovies_unique.csv',index=False,header=True)    #将最终的数据输出
print len(movies_unique)

def getScore(i):
    if i>=0 and i<6.0:
        return 0
    elif i>=6.0 and i<6.5:
        return 1
    elif i>=6.5 and i<7.0:
        return 2
    elif i>=7.0 and i<7.5:
        return 3
    elif i>=7.5 and i<8.0:
        return 4
    elif i>=8.0 and i<=10.0:
        return 5
    else: 
        return None

rate=movies_unique['rate']    #取出rate列
score=rate.map(getScore)   #对rate列应用getScore函数，得到score列
pd.options.mode.chained_assignment = None  # default='warn'
movies_unique['score']=score    #将score列添加到movies_unique
movies_unique.to_csv('doubanMovies_score.csv',index=False,header=True)    #将最终的数据输出