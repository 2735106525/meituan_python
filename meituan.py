# -- coding: utf-8 --
# *coding:utf-8 *
# 美团  已经锁定了小位置和分类，不用做token验证
# 目前这个版本是对cookie做的限制，爬取一定数量会封账号（过一段时间会撤销）

import requests
import csv
import time
import random

#UA池
def get_ua():
	user_agents = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
		'Opera/8.0 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
	]
	user_agent = random.choice(user_agents) #random.choice(),从列表中随机抽取一个对象
	return user_agent

#ip池
def ips():
    proxys = [
        {'HTTP': '120.83.111.161:9999'},
        {'HTTP': '122.138.139.53:9999'},
        {'HTTP': '117.69.12.249:9999'},
        {'HTTP': '171.35.175.181:9999'},
        {'HTTP': '171.13.137.137:9999'}
    ]
    proxy = random.choice(proxys)  # random.choice(),从列表中随机抽取一个对象
    return proxy

#Cookie池，还在更新
def get_cookies():
    cookies=[
        '''
        自己添加cookie
        '''
    ]
    cookie = random.choice(cookies)  # random.choice(),从列表中随机抽取一个对象
    return user_agent

#构造翻页网站
def nextpage():
    url1=[]
    start=0
    for i in range(0, 10):    #爬取多少页
        x = '&cateId=-1&q=%E6%B8%9D%E5%8C%97%E5%8C%BA%E6%B1%BD%E5%8D%9A%E4%B8%AD%E5%BF%83'
        urls = url + str(start) + x
        start += 32
        url1.append(urls)
    return url1

#UA  请求头
def headers(ua):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'apimobile.meituan.com',
        'Origin': 'https://cq.meituan.com',
        'Referer': 'https://cq.meituan.com/s/%E6%B8%9D%E5%8C%97%E5%8C%BA%E6%B1%BD%E5%8D%9A%E4%B8%AD%E5%BF%83/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua,
    }
    return headers

#解析数据并保存
def parsing(n,headers,ip):
    print(ip)
    res=requests.get(n,headers=headers,proxies=ip)
    for sj in res.json()['data']['searchResult']:
        title = sj['title']
        address = sj['address']
        phone = sj['phone']
        print(title,address,phone)
        writer.writerow((title, address, phone))    #保存数据
    time.sleep(10)                                  #数据有轻微重复做一个延迟

#启动
if __name__ == '__main__':
    fp = open('meituan_sj.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('商家名字', '商家地址', '商家电话'))

    url='https://apimobile.meituan.com/group/v4/poi/pcsearch/45?uuid=b66f403e6deb75a88ed9.1583475822.1.0.0&userid=-1&limit=32&offset='       #和nextpage()构成完整URL
    ns=nextpage()
    ua = get_ua()
    cookie=get_cookies()
    ip = ips()
    headers = headers(ua,cookie)
    for n in ns:
        parsing(n,headers,ip)