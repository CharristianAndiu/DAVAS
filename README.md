# Data Analysis Visiable Academic Search: Final Report of Course ICE2604-01 Group 9
#             Academic Search Final Report

## 项目总体概况

### 项目介绍

- 此次项目实现论文搜索的基础功能，可从三种搜索方式选择，输入后点击搜索框或Enter键返回搜索结果界面，也完成了图片解析以及表格解析功能，数据库共包含1300篇左右的论文，并做出了可视化表格。

### 小组分工

- 小组共五人，其中罗宇欣负责爬虫与数据库部分，俞昊沅负责搜索功能部分，孙浩然负责图片解析与表格解析部分，刘昌盛和唐渝杰负责前端网页与可视化部分。

### 整体语言

- 包括 Javascript， Python ， Html等，其中以 Javascript 为主。

### LOGO

![logo](C:\Users\刘昌盛\Desktop\AS网页\12.19v5.0\source\demo\assets\img\logo.png)



## ReadME

由于本次项目采用Http-server来处理静态文件的搜索与前端网页的响应，因此在运行文件之前，需要安装Node.js，并按照以下步骤在文件index.html路径下的命令行输入相关指令：

![image-20231230113051649](C:\Users\刘昌盛\AppData\Roaming\Typora\typora-user-images\image-20231230113051649.png)

- 打开文件后，在此界面打开cmd命令行
- 输入npm install -g http-server，第一次需要用npm包管理在本地下载http-server的相应文件，以后则可以跳过此步骤
- 输入http-server -a localhost -p 8080 -o index.html，然后即会自动运行打开即可。

下面附http-server相关指令及其含义：

![image-20231230113933791](C:\Users\刘昌盛\AppData\Roaming\Typora\typora-user-images\image-20231230113933791.png)



![image-20231230114011224](C:\Users\刘昌盛\AppData\Roaming\Typora\typora-user-images\image-20231230114011224.png)







## 各模块解析

### 爬虫与数据库部分

主要有3个部分：100篇PDF元数据数据库的存储，arXiv网页论文元数据和及其PDF的爬取，爬取的元数据的存储

#### 100篇PDF元数据数据库的存储：

- 通过python读取对应json文件远程连接数据库并且构建对应的表格和存入数据，数据处理提供的元数据json文件里的，还包括小组提取的PDF的图片表格的本地地址以及PDF文件的本地地址。

```py
import pymysql
import json

def createDB(name, _passwd):
    conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd=_passwd,
                        charset='utf8mb4')
    cr = conn.cursor()

    #创建数据库
    cr.execute(f'create database if not exists {name} character set utf8mb4 collate utf8mb4_general_ci')  # 如果不存在，则创建
    conn.commit
    conn.close()
    print("DATABASE created successfully!")
# 传输数据库的名称
def store_100_PDF(name, _passwd, filePath):
    conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd=_passwd,
                        db=name,
                        charset='utf8mb4')
    cr = conn.cursor()
    cr.execute('DROP TABLE IF EXISTS `100_PDF`')
    createTable = 'CREATE TABLE IF NOT EXISTS `100_PDF`( `paper_id` VARCHAR(255) NOT NULL, `title` TEXT , `author` TEXT, `abstract` TEXT, `journal` VARCHAR(255), `doi` VARCHAR(255), `link` VARCHAR(255), `date` DATETIME, `pdfPath` VARCHAR(255), `picture` VARCHAR(255), PRIMARY KEY (`paper_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 collate utf8mb4_general_ci'
    cr.execute(createTable)
    conn.commit()
    print("Table `100_PDF` created successfully!")


    metaData = json.load(open(filePath, encoding='utf-8'))
    for key in metaData.keys():
        data = metaData[key]
        paper_id = data['paper_id']
        title = data['title']
        print(len(title))
        author = json.dumps(data['author'])
        print(type(author))
        # x = input("PAUSING------------------------------------------------------------")
        abstract = data['abstract']
        journal = data['journal']
        doi = data['doi']
        link = data['link']
        date = data['date']
        pdfPath = "./bigHw/100_PDF/" + paper_id+".pdf"
        picture = "./bigHw/picture/" + paper_id + "/"
        cr.execute('INSERT INTO `100_PDF`(paper_id, title, author, abstract, journal, doi, link, date, pdfPath, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (paper_id, title, author, abstract, journal, doi, link, date, pdfPath, picture))
    conn.commit()
    print("100_PDF stored successfully!") 
```

主要注意点是注意PDF，以及图片放在合适的文件夹

#### arXiv网页论文元数据及PDF的爬取：

- 爬取了主要包括：cs，math，physics，economics，biology分类的供1300篇左右论文的元数据和PDF，将其保存到本地

```py
import requests
import feedparser
import json
import os
import time

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
    address = "./Economics/"+name
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


def getAllPDF(start):
    # arXiv API endpoint
    url = 'http://export.arxiv.org/api/query?'

    # 查询参数Blockchain
    params = {
    "search_query": "all: Economics OR all: Financial Cycle OR all: Economic Cycle OR all: Monetary Policy OR all: Financial Risk OR all: Supply Chain Finance" ,
    "start": start,  # 结果的起始索引
    "max_results": 50 #返回的最大结果数
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
        if(name in os.listdir('./Economics')):
            continue
        if getPDF(data['pdfLink'], name):
            with open('./Economics/metaData.json', 'a+', encoding='utf-8') as fp:
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write(",")
                fp.write('\n')

for i in range(200, 10000, 50):
    time.sleep(0.5)
    getAllPDF(i)
    print(f"start at {i} finished *********************************************************")
```

借用feedparser分析获取的元数据并且写入指定文件，注意点是网络代理的设置，可能因为网络代理连通性的原因，在爬取保存pdf过程中多次出现502错误代码，所以在保存数据的过程中我首先判断一下响应码是否为200，再进行保存，还要注意json格式的存储。

#### 爬取的元数据的存储

- 鉴于爬取数据获得的元数据和助教提供在属性上有差异，在数据库建了新表存储爬取到的论文的元数据和PDF的对应地址。

```py
def store_crwaler_PDF(name, _passwd):
    num = 0
    conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd=_passwd,
                        db=name,
                        charset='utf8mb4')
    cr = conn.cursor()
    cr.execute('DROP TABLE IF EXISTS `crawler_PDF`')
    createTable = 'CREATE TABLE IF NOT EXISTS `crawler_PDF`( `arXiv_ID` VARCHAR(255) NOT NULL, `title` TEXT , `author` TEXT, `abstract` TEXT, `Link` VARCHAR(255), `Published` VARCHAR(255), `pdfPath` VARCHAR(255), `Categories` TEXT, PRIMARY KEY (`arXiv_ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 collate utf8mb4_general_ci'
    cr.execute(createTable)
    conn.commit()
    print("Table `crwaler_PDF` created successfully!")

    DirPath = ['./biology/', './cs/', './Economics/', './math/', './physics/']
    for path in DirPath:
        metaData = json.load(open(path+'metaData.json', encoding='utf-8'))
        num += len(metaData)
        print(f'{path}: has data: {len(metaData)} =====================================')
        for data in metaData:
                paper_id = data['arXiv ID']
                title = data['title']
                author = json.dumps(data['author'])
                # x = input("PAUSING------------------------------------------------------------")
                abstract = data['abstract']
                link = data['Link']
                published = data['Published: ']
                pdfPath = path+ paper_id+".pdf"
                category =json.dumps(data['Categories'])
                cr.execute('INSERT INTO `crawler_PDF`(arXiv_ID, title, author, abstract, Link, Published , pdfPath, Categories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (paper_id, title, author, abstract, link, published, pdfPath, category))
    conn.commit()
    print("crawler_PDF stored successfully!") 
    print(num)
```

自己爬取数据的存储和100篇pdf的存储基本相似，主要的不同就是读取对应json文件后处理方式不同，这是因为写入文件时格式是列表+字典，和助教提供的有所区别



### 后端及搜索引擎部分

- 总体实现

  主要包括2个部分：创建相应的触发和切换搜索栏等功能；读取前端网页返回的搜索值，在本地文件夹里直接搜索具有对应关键词的数据然后返回。

- 实现的部分思路

  - 我们使用javascript为主要语言，首先读取了数据，读取JSON文件名列表和使用一个空数组来存储JSON数据。
  - 然后为每次的搜索结果条目创建HTML结构。funcResultPage 函数负责在页面上填充搜索结果。它从本地存储中检索搜索结果数据，并为每个结果条目创建 HTML 元素。
  - 我使用processJsonFiles函数从指定文件名中获得JSON数据，添加到jsonData数组中。
  - performSearch 函数用于根据用户输入执行搜索，并将结果存储在本地存储中。然后它要么调用funcResultPage，要么重定向到搜索结果页面。

- 代码展示

```javascript
//读取数据
// 存储所有JSON文件的文件名
const jsonFileNames = ['assets/data/biology.json', 'assets/data/CS.json',
    'assets/data/economics.json', 'assets/data/math.json',
    'assets/data/metaData.json', 'assets/data/physics.json','assets/data/Geo_metadata.json'];
// 存储读取到的JSON数据
let jsonData = [];
let resultList = [];

if (window.location.pathname.includes('searchResult')) {
    funcResultPage();
} else {
    localStorage.removeItem('resultListData');
}

// 创建一个函数来生成项目的 HTML 结构
function createResultItem(data) {
    const listItem = document.createElement('li');
    listItem.className = 'resultItem';

    const contentDiv = document.createElement('div');

    const titleElement = document.createElement('h3');
    titleElement.className = 'title';
    titleElement.textContent = data.title;

    const authorElement = document.createElement('p');
    authorElement.className = 'author';
    authorElement.textContent = '作者：' + data.author;

    const dateElement = document.createElement('p');
    dateElement.className = 'date';
    dateElement.textContent = '时间：' + data.date;

    const abstractElement = document.createElement('p');
    abstractElement.className = 'abstract';
    const abstractHeading = document.createElement('h4');
    abstractHeading.style.marginBottom = '5px';
    abstractHeading.textContent = '摘要：';
    const abstractText = document.createTextNode(data.abstract);
    abstractElement.appendChild(abstractHeading);
    abstractElement.appendChild(abstractText);

    const linkElement = document.createElement('a');
    linkElement.href = data.link;
    linkElement.className = 'link';
    linkElement.textContent = '了解更多';

    const pdfLinkElement = document.createElement('a');
    pdfLinkElement.href = data.pdfLink;
    pdfLinkElement.className = 'link pdfLink';
    pdfLinkElement.textContent = '浏览PDF文件';
    if (data.pdfLink === null) {
        pdfLinkElement.style.display = 'none'
    }

    const linkGroupDiv = document.createElement('div');
    linkGroupDiv.className = 'linkGroup';
    linkGroupDiv.appendChild(linkElement);
    linkGroupDiv.appendChild(pdfLinkElement);

    contentDiv.appendChild(titleElement);
    contentDiv.appendChild(authorElement);
    contentDiv.appendChild(dateElement);
    contentDiv.appendChild(abstractElement);
    if (data.paper_id!==null) {
        console.log(data)
        const assetLink = document.createElement('a');
        assetLink.href = `pageAsset.html?paper_id=${data.paper_id}`;
        assetLink.className = 'link assetLink';
        assetLink.textContent = '浏览文章部分插图';
        contentDiv.appendChild(assetLink);
        storePageInfo(data.paper_id,data.imgArray,data.eccelArray);
    }
    listItem.appendChild(contentDiv);
    listItem.appendChild(linkGroupDiv);
    return listItem;
}
// 生成结果内容
function funcResultPage() {
    const ul = document.querySelector('#ul');
    //清空搜索结果
    ul.innerHTML = '';
    const main = document.querySelector('.main');
    resultList = JSON.parse(localStorage.getItem('resultListData'));
    console.log(resultList)
    resultList.forEach((item) => {
        const data = {
            title: item.title,
            author: (typeof item.author) === 'string' ? item.author : item.author.join(','),
            date: item['Published: '],
            abstract: item.abstract,
            link: item.Link,
            pdfLink: item.pdfLink || null,
            paper_id: item.paper_id ? item.paper_id : null,
            imgArray : (item.imgArray && item.imgArray.length !== 0) ? item.imgArray : null,
            eccelArray :(item.eccelArray && item.eccelArray.length !== 0) ? item.eccelArray :undefined
         }
        const li = createResultItem(data);
        ul.appendChild(li);
    })
    main.style.height = ul.offsetHeight + 450 + 'px'
}
// 读取文件
async function processJsonFiles() {
    for (const fileName of jsonFileNames) {
        try {
            const response = await fetch(fileName);
            if (response.ok) {
                jsonData = [...jsonData, ...await response.json()];
                console.log(`已读取文件 ${fileName}`);
            } else {
                console.error(`读取文件 ${fileName} 时出错：${response.status}`);
            }
        } catch (error) {
            console.error(`读取文件 ${fileName} 时出错：${error.message}`);
        }
    }
}

// 调用函数开始处理JSON文件
processJsonFiles();

//搜索功能函数
function performSearch(id) {
    //清空搜索结果
    localStorage.removeItem('resultListData');
    resultList = [];
    let authorStr = '';

    let searchText = document.getElementById(id).value;
    if (id === 'input3') {
        jsonData.forEach(item => {
            console.log(item,typeof  item.author)
            if (typeof item.author === 'string') {
                authorStr = item.author
            } else {
                authorStr = item.author.join(',')
            }
            if (authorStr.includes(searchText)) {
                resultList.push(item)
            }
        })
    } else if (id === 'input2') {
        jsonData.forEach(item => {
            if (item.title.includes(searchText) || item.abstract.includes(searchText)) {
                resultList.push(item)
            }
        })
    } else {
        jsonData.forEach(item => {
            if (item.title.includes(searchText)) {
                resultList.push(item)
            }
        })
    }
    localStorage.setItem('resultListData', JSON.stringify(resultList));

    if (window.location.pathname.includes('searchResult')) {
        funcResultPage();
    } else {
        window.location.href = 'searchResult.html'
    }
}

//回车触发
function checkEnter(event, id) {
    if (event.keyCode === 13) { // 检查是否按下回车键（键码13）
        console.log(event)
        const inputValue = event.target.value.trim(); // 获取输入框的内容并去除前后空格
        if (inputValue !== '') { // 检查输入框内容是否不为空
            // 执行您的函数，例如触发搜索操作
            performSearch(id);
        }
    }
}
// 切换搜索栏
function switchSearch(value) {
    const {id, num, bgc} = value
    const searchBoxes = document.querySelectorAll('.searchInput');
    const menuBoxes = document.querySelectorAll('.menu');
    const header = document.querySelector('.header');
    searchBoxes.forEach(function (box) {
        if (box.id === id) {
            box.className = 'searchInput show';
        } else {
            box.className = 'searchInput';
        }
    });
    menuBoxes.forEach(function (item, index) {
        if (index === num) {
            item.className = 'menu on';
        } else {
            item.className = 'menu';
        }
    });
    header.style.backgroundColor = bgc
}
// 存储文章图片和表格的路径
function storePageInfo(paper_id,imgArray,eccelArray) {
    sessionStorage.setItem(paper_id,JSON.stringify({paper_id:paper_id,imgArray:imgArray,eccelArray:eccelArray}));
}

```

- 代码的一些可能的优点：
  - 使用了异步函数和fetch API来读取JSON文件，提高了代码的执行效率和用户体验。因为在JavaScript中，许多操作需要一定的时间才能完成，比如从服务器获取数据、读取文件、执行定时器等。为了避免阻塞主线程，使用了异步函数。
  - 利用localStorage和sessionStorage进行数据的存储，实现数据的持久化和共享。localStorage和sessionStorage都是Web浏览器提供的用于客户端存储数据的API，它们允许开发者在用户的浏览器中存储数据，以便在页面刷新或浏览器关闭后仍然可以访问这些数据。
  - 通过动态创建HTML元素的方式，实现了灵活的搜索结果页面生成和展示。
    使用了事件监听和条件判断来实现搜索触发和页面跳转。
    实践过程中可以提供更良好的用户体验，使搜索操作更加丝滑直观，即时地根据页面内容进行相应处理。

### 前端与可视化部分

#### 前端网页

- 网页介绍

  网页分三个页面，主页面Home，数据可视化网页
  Piture，项目介绍About，其中搜索后会跳转到结果展示页面。
  Home页面具有导航栏与搜索框，下部设计有轮播图展示论文网站的页面，其下我们设计了知名论文网站的链接，点击可以跳转到对应源网站。
  About页面是我们项目用到的资源的介绍，采用轮播图的形式，点击图片或者文字能跳转到我们用到的论文网站，可视化网站等资源。
  Picture页面是数据可视化的展示

- Home页面典型代码呈现

  Home主要是导航栏与搜索框部分，用div标签划分，其中均用无序列表ul标签盛放文字，图片与链接，并设置好class，结合css文件进行美化：

```html
<!--==================== HEADER ====================-->
<header class="header" id="header">
    <nav class="nav container">
        <a href="#" class="nav__logo">AS（Academic search）</a>
        <img src="assets/img/logo.png" alt="">
        <div class="nav__menu" id="nav-menu">
            <ul class="nav__list">
                <li class="nav__item">
                    <a href="index.html" class="nav__link" id="active">Home</a>
                </li>

                <li class="nav__item">
                    <a href="about.html" class="nav__link">About</a>
                </li>

                <li class="nav__item">
                    <a href="picture.html" class="nav__link">Picture</a>
                </li>
            </ul>

            <!-- Close button -->
            <div class="nav__close" id="nav-close">
                <i class="ri-close-line"></i>
            </div>

        </div>

        <div class="nav__actions">
            <!-- Search button -->
            <i class="ri-search-line nav__search" id="search-btn"></i>
        </div>
    </nav>
    <!--   搜索框-->
    <div class="search-container">
        <div class="switchBox">
            <div class="menu on" onclick="switchSearch({id:'searchInput1',num:0,bgc:'hsl(230, 100%, 98%)'})">标题搜索
            </div>
            <div class="menu" onclick="switchSearch({id:'searchInput2',num:1,bgc:'hsla(214,95%,84%,0.7)'})">关键词搜索
            </div>
            <div class="menu" onclick="switchSearch({id:'searchInput3',num:2,bgc:'hsla(207,82%,66%,0.74)'})">作者搜索
            </div>
        </div>
        <div class="inputGroup">
            <div class="searchInput show" id="searchInput1">
                <input type="text" class="search-input" id="input1" placeholder="请输入..."
                       onkeydown="checkEnter(event,'input1')">
                <button class="search-button" onclick="performSearch('input1')">搜索</button>
            </div>
            <div class="searchInput" id="searchInput2">
                <input type="text" class="search-input" id="input2" placeholder="请输入..."
                       onkeydown="checkEnter(event,'input2')">
                <button class="search-button" onclick="performSearch('input2')">搜索</button>
            </div>
            <div class="searchInput" id="searchInput3">
                <input type="text" class="search-input" id="input3" placeholder="请输入..."
                       onkeydown="checkEnter(event,'input3')">
                <button class="search-button" onclick="performSearch('input3')">搜索</button>
            </div>
        </div>
```

- About页面典型代码呈现

  本页面同样采用div与ul来装图片文字链接，其中每一个模块再用div装标题与简介，每一个标签设置好class便于css的渲染：

```html
<div class="page-wrapper" style="visibility: hidden;">
      <div class="list-wrapper">
         <div class="list">
            <a class="list-item" href="https://arxiv.org/">
               <figure class="project-figure">
                  <img src="assets/img/logo.png">
               </figure>
               <div class="project-info">
                  <h3>Arxiv</h3> 
                  <p>WebarXiv.org is a free online repository of preprints in various fields of physics and mathematics. </p>
               </div>
            </a>
            <a class="list-item" href="https://echarts.apache.org/zh/index.html">
               <figure class="project-figure">
                  <img src="assets/img/echarts.png">
               </figure>
               <div class="project-info">
                  <h3>Echarts</h3>
                  <p>An Open Source JavaScript Visualization Library.</p>
               </div>
            </a>
            <a class="list-item" href="https://github.com/facebookresearch/detectron2">
               <figure class="project-figure">
                  <img src="https://d1835mevib0k1p.cloudfront.net/portfolio/v2/images/progress-nav.png?1">
               </figure>
               <div class="project-info">
                  <h3>Detectron2</h3>
                  <p>Detectron2 is a platform for object detection, segmentation and other visual recognition tasks</p>
               </div>
            </a>
            <a class="list-item" href="https://github.com/npm/cli/releases/tag/v10.2.5">
               <figure class="project-figure">
                  <img src="https://d1835mevib0k1p.cloudfront.net/portfolio/v2/images/ladda.png">
               </figure>
               <div class="project-info">
                  <h3>Frontend related http-server</h3>
                  <p>Number of documents related to the processes, practices & overall operations of npm's Community & Open Source team.</p>
               </div>
            </a>
            <a class="list-item" href="https://lab.hakim.se/rymd">
               <figure class="project-figure">
                  <img src="https://d1835mevib0k1p.cloudfront.net/portfolio/v2/images/rymd.png?1">
               </figure>
               <div class="project-info">
                  <h3>Rymd</h3>
                  <p>Move your mouse or swipe to navigate the stars.</p>
               </div>
            </a>
            <a class="list-item" href="https://lab.hakim.se/spiral">
               <figure class="project-figure">
                  <img src="https://d1835mevib0k1p.cloudfront.net/portfolio/v2/images/spiral.png">
               </figure>
               <div class="project-info">
                  <h3>Spiral</h3>
                  <p>Interactive spiral animation.</p>
               </div>
            </a>
            
         </div>
      </div>
   </div>
```

- Picture页面代码介绍

  此部分代码与Home页面大体相同，都具有搜索功能与导航栏，其余的图标处理在可视化部分介绍。

#### 数据可视化

- 读取与储存数据

  用列表来储存读取到的数据，使用fetch()函数进行异步网络请求，并等待响应结果，如果成功则它使用response.json()将响应体解析为JSON格式的数据，并将整个数据数组data添加到jsonDataArr数组中，并记录数据的个数到subjectCounts数组中。再使用getDateData()函数处理subjectData数组，并将处理结果添加到subjectDataCountRow数组中。

```js
//读取的文件名数组
const jsonFileNamesArr = ['assets/data/biology.json', 'assets/data/CS.json',
    'assets/data/economics.json', 'assets/data/math.json', 'assets/data/physics.json','assets/data/Geo_metadata.json'];
const subjectArr = ['生物学', '计算机科学', '经济学', '数学', '物理学','地理学'];
//学科与时间与论文数量关系的未处理数据
let subjectDataCountRow = [];
//学科与时间与论文数量关系处理后的数据
let subjectDataCount = [];
let subjectCounts = [];
// 存储读取到的JSON数据
let jsonDataArr = [];
let yearsArr = [];
let yearsCounts = [];

async function processJsonFiles() {
    for (const fileName of jsonFileNamesArr) {
        try {
            const response = await fetch(fileName);
            if (response.ok) {
                const data = await response.json();
                const subjectData = data.map(item => {
                    return item['Published: ']
                })
                jsonDataArr = [...jsonDataArr, ...data];
                subjectCounts.push(data.length);
                subjectDataCountRow.push(getDateData(subjectData))
                console.log(`已读取文件 ${fileName}`, subjectDataCountRow);
            } else {
                console.error(`读取文件 ${fileName} 时出错：${response.status}`);
            }
        } catch (error) {
            console.error(`读取文件 ${fileName} 时出错：${error.message}`);
        }
    }
}
const getDateData = (dateData) => {
// 创建一个对象来存储年份计数
    let yearCount = {};
    // 遍历日期字符串数组
    dateData.forEach((dateString) => {
        // 使用正则表达式提取年份部分
        let yearMatch = dateString.match(/\d{4}/);
        if (yearMatch && yearMatch.length > 0) {
            let year = yearMatch[0];
            // 如果年份已经存在，则增加计数，否则初始化为1
            if (yearCount[year]) {
                yearCount[year]++;
            } else {
                yearCount[year] = 1;
            }
        }
    });

// 提取年份和计数，存储在数组中
    yearsArr = Object.keys(yearCount); // 年份数组
    yearsCounts = Object.values(yearCount); // 年份次数数组
    return yearCount
}
```

- 三个图表的设置

  - 第一张图表的属性

  ```js
  const option = {
        title: {
            text: '不同年份的论文数量',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            data: yearsArr,
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {},
        series: [
            {
                name: '论文数量',
                type: 'bar',
                data: yearsCounts,
                itemStyle: {
                    color: '#007afd'
                },
                label: {
                    show: true, // 启用数据标签
                    position: 'top' // 设置数据标签的位置，可以根据需要调整
                },
            }
        ]
    };
  ```

  - 第二张图表的属性

  ```js
  let option = {
        title: {
            text: '不同学科论文的数量占比',
            left: 'center'
  
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c}' + '篇' + ' ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: names
        },
        series: [
            {
                name: '学科占比',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: pieData,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
  ```

  - 第三张图表的属性

  ```js
  let option = {
        color: ['#80FFA5', '#00DDFF', '#37A2FF', '#FF0087', '#FFBF00','#845EC2'],
        title: {
            text: '各个学科文章数量随时间的变化关系'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data: legend,
            left: 520
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: xData
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '生物学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(128, 255, 165)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(1, 191, 236)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data:seriesData[0]
            },
            {
                name: '计算机科学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(0, 221, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(77, 119, 255)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[1]
            },
            {
                name: '经济学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(55, 162, 255)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(116, 21, 219)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[2]
            },
            {
                name: '数学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 0, 135)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(135, 0, 157)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[3]
            },
            {
                name: '物理学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 191, 0)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(224, 62, 76)'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[4]
            },
            {
                name: '地理学',
                type: 'line',
                stack: 'Total',
                smooth: true,
                lineStyle: {
                    width: 0
                },
                showSymbol: false,
                label: {
                    show: true,
                    position: 'top'
                },
                areaStyle: {
                    opacity: 0.8,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: '#845EC2'
                        },
                        {
                            offset: 1,
                            color: '#D65DB1'
                        }
                    ])
                },
                emphasis: {
                    focus: 'series'
                },
                data: seriesData[4]
            }
        ]
    };
  ```

### 图片解析与表格解析部分

#### 图片解析

定义函数 extract_images(pdf_path, output_folder)：

```python
def extract_images(pdf_path, output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_folder = os.path.join(output_folder, pdf_name)
    if not os.path.exists(pdf_output_folder):
        os.makedirs(pdf_output_folder)    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]            
            if '/Resources' in page and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()            
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        image = xObject[obj]
                        img_data = image._data
                        try:                            
                            img = Image.open(io.BytesIO(img_data))

                            img = img.convert('RGB')
                            
                            img_name = f"{pdf_name}_page{page_num + 1}_{obj[1:]}.png"
                            img_path = os.path.join(pdf_output_folder, img_name)
                            img.save(img_path, 'PNG')

                            print(f"Extracted: {img_name} from {pdf_name}")
                        except Exception as e:
                            print(f"Error extracting image from {pdf_name}, page {page_num + 1}, object {obj}: {e}")
            else:
                print(f"Page {page_num + 1} in {pdf_name} does not contain '/Resources' or '/XObject', skipping.")
```

通过PyPDF2打开PDF文件，获取文件名（不包含扩展名）作为输出文件夹的一部分。 创建一个以PDF名称为名的文件夹 遍历PDF的每一页，检查每一页的资源和XObject（对象的子类型）。 如果发现图像对象，尝试将其解码为图像。 将解码后的图像以PNG格式保存到指定的输出文件夹中。 遍历pdf文件，依次使用该函数提取图片并且保存在对应文件夹。



#### 表格解析

表格提取主要分为两个部分:表格定位和表格提取。

##### 表格定位

主要使用了给定的detectron插件,该插件在定位表格上表现良好,主要问题是运行时需要很长时间,原因在于给定代码只使用了cpu,修改代码使其使用cuda,利用gpu后运行速率显著提高:

```python
state_dict = torch.load(weight_path, map_location=torch.device('cuda'))
cfg.MODEL.DEVICE = "cuda"
```

##### 表格提取

- ##### 跑通代码后发现，基础代码主要问题在于：

1. 无法识别负号以及特殊字符（如希腊字母等）

2. 上下标不能正常显示，全部显示为正常的数字。

3. 列分隔存在缺陷，有两列合并的情况。

   

- ##### 问题解决:

​      (1)关于负号以及特殊字符，查阅官方文档发现camelot的read_pdf函数默认输出为csv格式，于是引入pandas库，提取表格的pandas dataframe，再次输出，可以显示正确的字符形式：

```python
df_pandas = df.df
# 保存到 Excel
df_pandas.to_excel(os.path.join(output_table_dir, f'output_{page_id + 1}_{idx + 1}.xlsx'), index=False)
```

​       (2)上下标：在提取过程中，首先使用read_pdf的flag_size参数，可以标记出上下标数字的位置，该标记显示为 `<s>123<\s>`在excel里无法直接转化为上下标，于是对提取的表格内容进行后处理，定义convert_to_superscript函数：

```python
def convert_to_superscript(text):
    def repl(match):
        num_or_char = match.group(1)
        superscript_nums = str.maketrans("0123456789abcdefghijklmnopqrstuvwxyz", "⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ")
        return num_or_char.translate(superscript_nums)

    return re.sub(r'<s>(\w+)<\/s>', repl, text)
```

将<s></s>标记的元素转换为上下标形式。
      (3)参阅camelot官方文档，列分割缺陷的可能原因是读取的pdf文档中缺少分隔符（空格），又可见列分割的重灾区为负数，例如100;-100被识别为整体的100-100,于是想到对表格进行预处理，在负号“-”前自动加上空格，以便于camelot识别负号的间隔：

```python
def preprocess_pdf_text(self, text):
    # 在负号前添加空格
    processed_text = re.sub(r'(?<=\d)-', ' -', text)
    return processed_text
```

添加空格后进行分割，有一些成功分开，其余表格，修改read_pdf的各类参数，如edge_tol,shift_text,flavour,split_line,split_text等，效果不是很好，尝试使用ocr(tesseract)效果比camelot提取稍差，最终决定仍然使用camelot读取表格。



## 写在最后

感谢老师及助教的耐心指导，也感谢每位组员的付出，这是我们第一次尝试做一个需要分工明确的项目，中间也遇到很多问题，中间也租借服务器，可是最后只是传上文件，因为选择处理静态文件的原因，也相当于没有使用。同时最后也有许多设想的功能没有来得及实现，但也算最终做成，对此类项目积累了部分经验，也更熟悉所学知识，有所收获。

我们在GitHub上的repo :   [CharristianAndiu/DAVAS (github.com)](https://github.com/CharristianAndiu/DAVAS)

我们的服务器地址：http://60.204.147.167:34840/fc4faf69

- 账号：wiuw42lg
- 密码：921c7c13
