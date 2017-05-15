# -*- coding: utf-8 -*-
'''
该段代码通过step2_getScore.py得到的doubanMovies_score.csv文件中的每个豆瓣电影的网址
获取每个豆瓣电影的页面内容信息
得到directors导演、leadingRoles主演、releaseDate上映日期
alterNames又名、IMDBurl对应的IMDB链接等信息
'''

from getInfoOfOneMovie_functions import *  # 从getInfoOfOneMovie_functions脚本中引入自己定义的函数
doubanMovies_score = pd.read_csv('doubanMovies_score.csv')
allUrls = doubanMovies_score['url']

movieInfo = DataFrame({'directors': [], 'leadingRoles': [],
                       'releaseDate': [], 'alterNames': [], 'IMDBurl': []})
csvFileName = 'doubanMovies_scoreInfoAdded.csv'  # 包含豆瓣电影对应的IMDB网址的数据文件
errorStartPoint = 1  # 为了方便做错误标记，增加该参数，表示上一次运行到哪部电影出错
unknownError = DataFrame({'directors': ['unknownError'], 'leadingRoles': ['unknownError'], 'releaseDate': [
                         'unknownError'], 'alterNames': ['unknownError'], 'IMDBurl': ['unknownError']})  # 出现严重错误时添加该字符串，为了方便添加，所以使用DataFrame格式
for i in range(errorStartPoint - 1, len(allUrls)):
    try:
        movieInfo = appendOne(movieInfo, str(allUrls[i]))
        print len(movieInfo) + errorStartPoint - 1
    except:
        movieInfo = pd.concat([movieInfo, unknownError])
        print len(movieInfo) + errorStartPoint - 1, 'with unknownError added'
    finally:
        movieInfo.to_csv(csvFileName, index=False, encoding='utf-8')
