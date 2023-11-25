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
def storePDF(name, _passwd, filepath):
    conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd=_passwd,
                        db=name,
                        charset='utf8mb4')
    cr = conn.cursor()
    cr.execute('DROP TABLE IF EXISTS `PDF`')
    createTable = 'CREATE TABLE IF NOT EXISTS `PDF`( `paper_id` VARCHAR(255) NOT NULL, `title` TEXT , `author` TEXT, `abstract` TEXT, `journal` VARCHAR(255), `doi` VARCHAR(255), `link` VARCHAR(255), `date` DATETIME, PRIMARY KEY (`paper_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 collate utf8mb4_general_ci'
    cr.execute(createTable)
    conn.commit()
    print("Table `PDF` created successfully!")


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
        cr.execute('INSERT INTO `PDF`(paper_id, title, author, abstract, journal, doi, link, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (paper_id, title, author, abstract, journal, doi, link, date))
    conn.commit()
    print("Data stored successfully!") 








if __name__ == '__main__':
    #!=====================================================================================================================
    _passwd = '11111'    # 输入你自己的密码
    filePath = './大作业补充材料/100_PDF_MetaData.json' #将其换为文件所在的路径
    name = 'BigHw' # 输入你数据库的名字（！！！注意不是table的名字）s
    # table 名字默认 `PDF`
    #!======================================================================================================================
    createDB(name, _passwd)
    storePDF(name, _passwd, filePath)        











