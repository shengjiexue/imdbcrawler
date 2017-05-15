# -*- coding: utf-8 -*-
from pandas import DataFrame
import pandas as pd


def getScore(i):
    if i >= 0 and i < 6.0:
        return 0
    elif i >= 6.0 and i < 6.5:
        return 1
    elif i >= 6.5 and i < 7.0:
        return 2
    elif i >= 7.0 and i < 7.5:
        return 3
    elif i >= 7.5 and i < 8.0:
        return 4
    elif i >= 8.0 and i <= 10.0:
        return 5
    else:
        return None
###################################################
# 将IMDB评分转换为5分制
# df=pd.read_csv('doubanMovies_IMDB.csv')
# score_IMDB=[]
# for i in range(len(df)):
#    if df.ix[i,'IMDBRate']!='No Rating' and df.ix[i,'IMDBRate']!='-':
#        score_IMDB.append(getScore(float(df.ix[i,'IMDBRate'])))
#    else:
#        score_IMDB.append(df.ix[i,'IMDBRate'])
#
# df['score_IMDB']=score_IMDB
# df.to_csv('doubanMovies_IMDBScore.csv')
###################################################

############################################################################
# 将豆瓣和IMDB的rate合并，并配置权重
# 如果没有相应的IMDB链接，或者有IMDB链接，但是没有评分
# 则合并后的rate就采用豆瓣的rate
# 最后将合并后的rate转化为5分制
df = pd.read_csv('doubanMovies_IMDBScore.csv')
weight_douban = 0.5  # 豆瓣的rate的权重值
weight_IMDB = 1 - weight_douban  # IMDB的rate的权重值
rate_doubanAndIMDB = []  # 初始化合并后的rate列表
score_final = []  # 初始化最终的评分列表

# 得到豆瓣rate和IMDBRate加权后rate_doubanAndIMDB列表
for i in range(len(df)):
    df.ix[i, 'rate'] = float(df.ix[i, 'rate'])  # 为防止出错，再加这么一句
    if df.ix[i, 'IMDBRate'] != 'No Rating' and df.ix[i, 'IMDBRate'] != '-':
        df.ix[i, 'IMDBRate'] = float(df.ix[i, 'IMDBRate'])  # 将数据集中的IMDBRate数据转换为float格式
        # 将rate和IMDBRate进行加权
        temp = weight_douban * (df.ix[i, 'rate']) + weight_IMDB * (df.ix[i, 'IMDBRate'])
        # 将加权后的rate值加入到 rate_doubanAndIMDB列表中
        rate_doubanAndIMDB.append(temp)
    else:
        # 如果没有IMDB链接或IMDB没有评分，则直接使用豆瓣的rate值
        rate_doubanAndIMDB.append(df.ix[i, 'rate'])

# 利用加权后的rate值得到最终的分数值score_final列表
for i in range(len(df)):
    score_final.append(getScore(rate_doubanAndIMDB[i]))

df['rate_doubanAndIMDB'] = rate_doubanAndIMDB
df['score_final'] = score_final
df.to_csv('test.csv', index=False)
############################################################################
