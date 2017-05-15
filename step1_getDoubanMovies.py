# -*- coding: utf-8 -*-
'''
该脚本得到豆瓣上所有电影的如下信息：
"rate": "7.5",
"cover_x": 2000,
"is_beetle_subject": false,
"title": "鬼乡",
"url": "https://movie.douban.com/subject/26322928/",
"playable": false,
"cover": "https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p2226663805.jpg",
"id": "26322928",
"cover_y": 2820,
"is_new": false
并保存为csv格式和js格式，但是未去重
'''
import requests  # 此处采用requests方法得到网页响应
import json
import time
from pandas import DataFrame


def getTagData(tag):
    data_oneTag = []  # 待添加数据列表
    page_start = 0  # 起始页
    data_oneSubject = [1]  # 为了冷启动，使data_oneSubject不为空
    # 设置代理
    # proxies={ "http": "http://115.159.96.136:1080"}
    # 设置User-Agent
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    # 当data_oneSubject不为空，也就是始终可以从网页中获取内容时，不停循环
    while(data_oneSubject != []):
        # 通过修改tag和page_start来不断的修改网址
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=' + \
            tag + '&sort=recommend&page_limit=20&page_start=' + str(page_start)
        resp = requests.get(url, headers=headers)
        # resp=requests.get(url,proxies=proxies,headers=headers)  #发出获取内容请求，得到的resp.text为json字符串
        # 将json字符串resp.text转换成Python形式，得到的data_oneSubject整体为一个键为'subjects'的长度为1的字典
        data_oneSubject = json.loads(resp.text)
        data_oneSubject = data_oneSubject['subjects']  # 取出data_oneSubject字典中键'subjects'对应的值，为20个字典
        data_oneTag += data_oneSubject  # 将data_oneSubject添加到data_oneTag数据中
        page_start += 20  # 起始页增加20
        time.sleep(1)  # 为了避免请求的太频繁被封掉IP，所以每次循环都要暂停一秒
    return data_oneTag  # 返回标签为tag时所有获得的数据

data_allTag = []  # 待添加所有标签的数据集列表
moviesNum = 0  # 所有标签下的电影总数，该数字没有消除重复项
# for tag in ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '治愈']:
for tag in ['美国']:
    print tag
    data_oneTag = getTagData(tag)  # 针对每个标签调用getTagData函数
    data_allTag += data_oneTag  # 将每个标签下的得到的数据加入到data_allTag数据集中，最终的data_allTag为数据list数据结构，每一项为一个字典
    moviesNum += len(data_oneTag)  # 计算所有标签下电影的总数（包含重复项）
    print tag + ':', len(data_oneTag)  # 打印出各个标签下得到的电影数

print '电影总数为:', moviesNum  # 打印出总电影数，该数字没有消除重复项
for i in range(5):
    # 打印出data_allTag的前10项，只输出键'title'和'rate'对应的值
    print data_allTag[i]['title'] + ' ' + data_allTag[i]['rate']

df = DataFrame(data_allTag)

# title列为unicode编码格式，在将数据输出为csv格式时会出现编码问题，所以下面三行将title列数据转换为utf-8格式
title = df['title']
title = title.map(lambda x: x.encode('utf-8'))
df['title'] = title

# 将结果中rate列的数字转换为float格式
rate = df['rate']  # 将df的rate列取出，格式为Series
rate = rate.map(float)  # 将rate列中的数值转换为float格式
df['rate'] = rate  # 将df中的rate列替换为float格式的rate列

# 将DataFrame格式的结果数据写入csv格式的文件中
df.to_csv('IMDBMovies.csv', index=False, header=True)

# #将数据结构为list的data_allTag转换成json格式后保存到doubanMovie.js文件中
# try:
#     f1=open('doubanMovies.js','w')
#     f1.write(json.dumps(data_allTag))    #将list数据结构的data_allTag写入json文件
# except:
#     print '写入js文件未成功！'
# finally:
#     f1.close()    #注意关闭文件流
