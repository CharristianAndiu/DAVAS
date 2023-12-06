import requests
import feedparser
import json
import os

headerLst = ['Mozilla/h5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
             ]

_headers = {
            'Accept': '*/*', 
            'User-Agent': headerLst[1]
            }

#! 设置代理，本机已经使用代理软件
proxy = '127.0.0.1:7890'
_proxies = {
    'http': 'http://' + proxy,
    'https': 'http://'+proxy
}

#! 测试使用
# # 国外
# url = 'http://arxiv.org/pdf/2311.12061.pdf'
# url2 = "http://arxiv.org/pdf/2207.13666v3.pdf"
# url3 = "http://arxiv.org/pdf/2106.01016v2"
# # 国内
# url1 = 'https://corporate.exxonmobil.com/-/media/Global/Files/worldwide-giving/2018-Worldwide-Giving-Report.pdf'




#! name 是以.pdf结尾的字符串(文件地址)
def getPDF(url, name):
    address = "./crawlerSource/"+name
    print()
    print(f"URL: {url}")
    _response = requests.get(url=url, headers=_headers, proxies=_proxies, verify=False)
    print(_response.status_code)
    if _response.status_code != 200:
        return False
    with open(address, 'wb') as f:
        f.write(_response.content)
    print(f"==================={name} has been saved!!===================")
    return True

#! 测试使用
# getPDF(url, "test1.pdf")
# getPDF(url2, 'test2.pdf')
# getPDF(url3, "test3.pdf")


def getAllPDF():
    # arXiv API endpoint
    url = 'http://export.arxiv.org/api/query?'

    # 查询参数
    params = {
    "search_query": "all:SAC OR all:DDPG OR all:DQN" ,  # 搜索所有包含"SAC, DDPG, DQN"的论文
    "start": 60,  # 结果的起始索引
    "max_results": 100  # 返回的最大结果数
    }

    # 发送GET请求
    response = requests.get(url, params=params)

    # 解析返回的XML数据
    feed = feedparser.parse(response.content)

    # 打印每篇论文的元数据
    for entry in feed.entries:
    # print(entry)
    # print(type(entry))
    # print()
    # print('Title: ', entry.title)
    # print()
    # print('Summary: ', entry.summary)
    # print()
    # print('Published: ', entry.published)
    # print()
    # print('Authors: ', [author.name for author in entry.authors])
    # print()
    # print('Link: ', entry.link)
    # print()
    # print('PDF Link: ', entry.links[1]['href'])
    # print('arXiv ID: ', entry.id.split('/')[-1])
    # print()
    # print('Categories: ', [t['term'] for t in entry.tags])
    # print()
    # print('---')
        for _dict in entry.links:
            if('title' in _dict and _dict['title'] == 'pdf'):
                pdfLink = _dict['href']
                break
            pdfLink = ''
        if(pdfLink == ''):
            continue
        data = {
            'title': entry.title,
            'Published: ': entry.published,
            'abstract': entry.summary,
            'author': [author.name for author in entry.authors],
            'pdfLink': pdfLink+'.pdf',
            'Categories': [[t['term'] for t in entry.tags]],
            'Link': entry.link,
            'arXiv ID': entry.id.split('/')[-1]     
            }
        name = data['arXiv ID']+'.pdf'
        if(name in os.listdir('./crawlerSource')):
            continue
        if getPDF(data['pdfLink'], name):
            with open('./crawlerSource/metaData.json', 'a+', encoding='utf-8') as fp:
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write('\n')

getAllPDF()


