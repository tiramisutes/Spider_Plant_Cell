#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: 许忠平
@license: Apache Licence
@contact: 1099808298@qq.com
@site: http://tiramisutes.github.io/
@software: python3.6
@time: 2020/5/10 18:46
@description：爬取 Plant Cell 创刊到现在发表的Articles文章标题和链接，并调用百度翻译API将标题翻译成中文
"""

import requests
from lxml import etree
import time
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from wordcloud import STOPWORDS
# Translator Fanyi (have limit)
# from translate import Translator
# Baidu Fanyi
import random
import re
import json
import requests
import hashlib


#################################################################################
#################################### 定义变量 ####################################
#################################################################################
# 主页地址
BASE_DOMAIN = 'http://www.plantcell.org'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

# Biadu Fanyi API，填写自己帐号的信息
appid = ''
secretKey = ''

#################################################################################
#################################### 定义函数 ####################################
#################################################################################

def get_md5(string):
    hl = hashlib.md5()
    hl.update(string.encode('utf-8'))
    return hl.hexdigest()

def baidu_en_to_zh(en_str):
    '''
    连续翻译太频繁会使 <result.get('trans_result')> 为空
    而出现报错：TypeError: 'NoneType' object is not subscriptable
    所以，让每翻译一次 sleep 3 秒
    '''
    api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768,65536)
    sign = get_md5(appid + en_str + str(salt) + secretKey)
    api_data = {
      'q':en_str,
      'from':'en',
      'to':'zh',
      'appid':appid,
      'salt':salt,
      'sign':sign
      }
    req_get = requests.get(api_url,api_data)
    result = req_get.json()
    lis = result.get('trans_result')
    Fanyi_result = lis[0].get('dst')
    time.sleep(5)
    return Fanyi_result


def youdao_en_to_zh(word):
    '''
    有道翻译感觉没有百度翻译的好
    '''
    appVersion = '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    #浏览器调试后发现ts是时间戳
    ts = str(int(time.time()*1000))
    #bv是请求头里面浏览器的信息经过MD5加密
    bv = hashlib.md5(appVersion.encode('utf-8')).hexdigest()
    #salt是时间戳后面随机加一位数字[0,9]
    salt = ts + str(random.randint(0,9))
    sign_str = "fanyideskweb" + word + salt + "@6f#X3=cCuncYssPsuRUE"
    #sign是上面这个字符串MD5后的结果
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    #request请求地址
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    #请求头
    headers = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Content-Length":"258",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"OUTFOX_SEARCH_USER_ID=1011964969@10.169.0.83; JSESSIONID=aaa2xaVAnC78n4KVSHwUw; OUTFOX_SEARCH_USER_ID_NCOO=280669685.8154466; ___rl__test__cookies=1561601226382",
    "Host":"fanyi.youdao.com",
    "Origin":"http://fanyi.youdao.com",
    "Referer":"http://fanyi.youdao.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
    }
    #请求数据，json字符串，其中salt，sign，ts,bv的值每次请求都会变
    data = {
    "i":word,
    "from":"AUTO",
    "to":"AUTO",
    "smartresult":"dict",
    "client":"fanyideskweb",
    "salt":salt,
    "sign":sign,
    "ts":ts,
    "bv":bv,
    "doctype":"json",
    "version":"2.1",
    "keyfrom":"fanyi.web",
    "action":"FY_BY_CLICKBUTTION"
    }
    response = requests.post(url, data=data, headers=headers)
    ret = response.text
    #正则匹配到需要的翻译结果
    dict_ret = json.loads(ret)
    translateResult = dict_ret.get("translateResult")
    Result = translateResult[0][0].get("tgt")
    time.sleep(3)
    return Result


def parse_detail_page(year_star, year_end, trantool):
    films = {}
    for i in ['year', 'title', 'china_title', 'Articles_URL']:
        if i not in films:
            films[i] = []
    for year in range(year_star, year_end):
        # Get year URLs
        print("="*80)
        print('= Begain to spider articles in {} year ='.format(year))
        year_page_url = BASE_DOMAIN + "/content/by/year/" + str(year)
        print('= This year URL is ' + year_page_url + ' =')
        response = requests.get(year_page_url, headers=HEADERS)
        html_element = etree.HTML(response.text)
        detail_urls = html_element.xpath('//div[@class="archive-issue-list"]//div[@class="highwire-cite-metadata"]//a/@href')
        detail_urls = map(lambda x: BASE_DOMAIN + x, detail_urls)
        ############################################
        # parse each year URLs
        count = 0
        for url in list(detail_urls):
            print('= Begain to spider articles in {} site ='.format(url))
            response = requests.get(url, headers=HEADERS)
            text = response.content.decode('utf-8')
            soup = BeautifulSoup(text,'lxml')
            sections = ['in-brief', 'large-scale-biology-articles', 'research-articles']
            for jump in sections:
                aa = soup.find('div', class_='issue-toc-section issue-toc-section-{}'.format(jump))
                #print(type(aa))
                if isinstance(aa,bs4.element.Tag): 
                    bb = aa.find_all('a', class_ ='highwire-cite-linked-title')
                    for index in range(0, len(bb)):
                        title = bb[index].get_text()
                        #print(title)
                        #translator = Translator(to_lang="chinese")
                        #china_title = translator.translate(title)
                        if trantool == "baidu":
                        	china_title = baidu_en_to_zh(title)
                        elif trantool == "youdao":
                        	china_title = youdao_en_to_zh(title)
                        url = bb[index].get('href')
                        url = BASE_DOMAIN + url
                        films['year'].append(year)
                        films['title'].append(title)
                        films['china_title'].append(china_title)
                        films['Articles_URL'].append(url)
                        count = count + 1
        print("Total publish \033[1;35m" + str(count) + "\033[0m articles in {} year".format(year))
        print("="*80)
        time.sleep(1)
    return films


def save_to_csv(dictdata, filename):
    '''
    encoding='utf-8_sig' 解决保存csv中文乱码问题
    '''
    df = pd.DataFrame.from_dict(dictdata)
    df = df.sort_values(by=['title', 'title'])
    df.to_csv(filename, sep=',', header=True, index=False, encoding='utf-8_sig')


def pcwordcloud(text, exclude, filename):
    '''
    text: 输入要展示的文本
    exclude: 需要排除的单词
    filename: 保存图片名称
    参考：https://www.datacamp.com/community/tutorials/wordcloud-python
    '''
    print("#"*80)
    print ("There are {} words used to create this WordCloud.".format(len(text)))
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(exclude)
    #stop_words = exclude + list(STOPWORDS)
    wordcloud = WordCloud(
        background_color = "white",
        width = 1500,
        height = 960,
        margin = 10,
        #stopwords = stop_words
        stopwords = stopwords
        ).generate(text)
    # store to file
    wordcloud.to_file(filename)
    print("The WordCloud ({}) is plot for all articles titles in Plant Cell.".format(filename))
    print("#"*80)


def spider():
    tool = "baidu"  # baidu or youdao
    film = parse_detail_page(1989, 2021, tool)
    print("Select use {} translator to translate this english titles to chinese titles".format(tool))
    num = len(film.get("title"))
    print("Total publish \033[0;36m" + str(num) + "\033[0m articles in 1989-2020 year")
    save_to_csv(film, tool + "Plant_Cell_Articles.csv")
    text = " ".join(film.get("title"))
    exclude = ['plant', 'gene', 'expression', 'Are', 'protein', 'and', 'of', 'in', 'the', 'is', 'with' 'from', 
               'sequence', 'analysis', 'two', 'cell', 'Different']
    pcwordcloud(text, exclude, tool + "Plant_Cell_Articles.png")


if __name__ == '__main__':
    spider()
