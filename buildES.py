import json
import pymysql
from elasticsearch import Elasticsearch

es = Elasticsearch()
print(es.ping())


geo_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "identifier": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "date": {
                "type": "date",
            },
            "ref_paper": {
                "type": "text",
                "analyzer": "simple"
            },
            "conference": {
                "type": "text",
            },
            "keywords": {
                "type": "text",
            },
            "year": {
                "type": "long",
            },
            "author":{
                "affiliation":{
                    "type":"text"
                },
                "name":{
                    "type":"text"
                }
            },
            "last_page":{
                "type":"long"
            },
            "link":{
                "type":"text"
            },
            "abstract":{
                "type":"text"
            },
            "title":{
                "type":"text"
            },
            "paper_id":{
                "type":"text"
            },
            "volume":{
                "type":"text"
            },
            "update_time":{
                "type":"date"
            },
            "journal":{
                "type":"text"
            },
            "issn":{
                "type":"text"
            },
            "first_page":{
                "type":"long"
            },
            "publisher":{
                "type":"text"
            },
            "doi":{
                "type":"text"
            },
        }
    }
}

users_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            "userId": {
                "type": "keyword",
            },
            "userName": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "socialComment": {
                "type": "text",
            },
            "profileImageUrl": {
                "type": "keyword",
            },
            "paper_id": {
                "type": "text",
            },

        }
    }
}

es.indices.create(index='papers_index', body=geo_mappings)
es.indices.create(index='users_index', body=users_mappings)

try:
    conn = pymysql.connect(host="101.132.109.217",
                            port=3306,
                            user="ieei",
                            passwd="Diangongdao_B",
                            charset="utf8",
                            db="Final_Homework")
    cursor = conn.cursor()
except:
    print('Fail to connect to the database.')

cursor.execute('SELECT * FROM ###')#等有表了再改表名
content = cursor.fetchall()

# 导入数据
id=0
for i in content:
    elem = {

        "id": i[0],
        "identifier": i[1],
        "date": i[2],
        "ref_paper": i[3],
        "conference":i[4],
        "keywords": i[5],
        "author": i[6],
        "last_page": i[7],
        "link": i[8],
        "abstract": i[9],
        "title": i[10],
        "paper_id":i[11],
        "volume": i[12],
        "update_time": i[13],
        "journal":i[14],
        "issn":i[15],
        "first_page":i[16],
        "publisher":i[17],
        "doi": i[18],

    }
    es.index(index="papers_index", id=id, body=elem)
    id += 1

cursor.execute('SELECT * FROM ####')
content = cursor.fetchall()

id = 0
for i in content:
    elem = {


        "userId":i[0],
        "userName": i[1],
        "socialComment": i[2],
        "profileImageUrl": i[3],
        "paper_id": i[4],

    }
    es.index(index="users_index", id=id, body=elem)
    id += 1
