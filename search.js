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


