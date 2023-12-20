from curses import meta
from unicodedata import category
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



def store_crwaler_PDF(name, _passwd):
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
                print(category)
                cr.execute('INSERT INTO `crawler_PDF`(arXiv_ID, title, author, abstract, Link, Published , pdfPath, Categories) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (paper_id, title, author, abstract, link, published, pdfPath, category))
    conn.commit()
    print("crawler_PDF stored successfully!") 








if __name__ == '__main__':
    #!=====================================================================================================================
    _passwd = ''    # 输入你自己的密码
    filePath = './bigHw/100_PDF_MetaData.json' #将其换为文件所在的路径
    name = 'BigHw' # 输入你数据库的名字（！！！注意不是table的名字）s
    # table 名字默认 `PDF`
    #!======================================================================================================================
    # createDB(name, _passwd)
    # store_100_PDF(name, _passwd, filePath)        
    store_crwaler_PDF(name, _passwd)












