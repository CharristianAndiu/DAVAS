
import json
import pymysql
from elasticsearch import Elasticsearch

es = Elasticsearch()



print(es.ping())
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user="root",
                       passwd="123456",
                        db="bigwork",
                       charset="utf8mb4"
                       )
cursor = conn.cursor()
sql = "SELECT * FROM crawler_pdf"
cursor.execute(sql)

results = cursor.fetchall()


all_mappings = {
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
            "arXiv_ID": {
                "type": "text",
                "analyzer": "cjk_analyzer"

            },
            "title": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "abstract": {
                "type": "text",
                "analyzer": "simple"
            },
            "author": {
                "type": "text",
            },
            "Published": {
                "type": "text",
            },
            "Link": {
                "type": "text",
            },

            "pdfPath":{
                "type":"text"
            },
            "Categories": {
                "type": "text"
            }

        }
    }
}
indexname = 'all_index'
#依据mapping创建索引
es.indices.create(index=indexname,body=all_mappings,ignore=400)

# 导入数据
id=0
for i in results:
    elem = {
        "arXiv_ID": i[0],
        "title": i[1],
        "author": i[2],
        "abstract": i[3],
        "Link": i[4],
        "Published": i[5],
        "pdfPath": i[6],
        "Categories": i[7],

    }
    # print(i[6])

    es.index(index=indexname, id=id, body=elem)
    # print(i)
    id += 1


cursor.close()
conn.close()

#关闭es连接
es.close()

