import decimal
import json
import pymysql
from elasticsearch import Elasticsearch
from decimal import Decimal
from datetime import datetime,date
es = Elasticsearch()
import datetime
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        # 处理返回数据中有date类型的数据
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        # 处理返回数据中有datetime类型的数据
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # 处理返回数据中有decimal类型的数据
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            print("MyEncoder-datetime.datetime")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        #elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

print(es.ping())
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user="root",
                       passwd="123456",
                        db="bigwork",
                       charset="utf8mb4"
                       )
cursor = conn.cursor()
sql = "SELECT * FROM pdf"
cursor.execute(sql)
data=[]
results = cursor.fetchall()
for row in results:
    data.append(row)
data=json.dumps(data ,indent=4,ensure_ascii=False, cls=DateEncoder).encode("utf-8")
print(data)
with open("output.json", 'w') as write_f:
    write_f.write(str(data))


es = Elasticsearch()
# print(results)
geography_mappings = {
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
            "paper_id": {
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
            "journal": {
                "type": "text",
            },
            "doi": {
                "type": "text",
            },
            "link": {
                "type": "text",
            },

            "date":{
                "type":"date"
            }

        }
    }
}
#
# users_mappings = {
#     "settings": {
#         "index": {
#             "analysis": {
#                 "analyzer": {
#                     "cjk_analyzer": {
#                         "type": "custom",
#                         "tokenizer" : "icu_tokenizer"
#                     }
#                 }
#             }
#         }
#     },
#     "mappings" : {
#         "properties": {
#             "author":{
#                 "affiliation":{
#                     "type":"text"
#                 },
#                 "name":{
#                     "type":"text"
#                 }
#             },
#             "paper_id": {
#                 "type": "text",
#                 "analyzer": "cjk_analyzer"
#
#             }
#
#         }
#     }
# }
indexname = 'index'
#依据mapping创建索引
es.indices.create(index=indexname,body=geography_mappings,ignore=400)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        # 处理返回数据中有date类型的数据
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        # 处理返回数据中有datetime类型的数据
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # 处理返回数据中有decimal类型的数据
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


s=""
# 导入数据
id=0
for i in results:
    elem = {
        "paper_id": i[0],
        "title": i[1],
        "author": i[2],
        "abstract": i[3],
        "journal": i[4],
        "doi": i[5],
        "link": i[6],
        "date": i[7],

    }
    # print(i[6])

    es.index(index=indexname, id=id, body=elem)
    # print(i)
    id += 1

    new_str = json.dumps(str(elem),indent=4).replace("'", '"')
    print(new_str)
    s =s+new_str
# with open("output.json", 'w') as write_f:
#     write_f.write(s)
cursor.close()
conn.close()

#关闭es连接
es.close()
# cursor.execute('SELECT * FROM bigwork')
# content = cursor.fetchall()
#
# id = 0
# for i in content:
#     elem = {
#
#
#         "author":i[0],
#         "paper_id": i[1]
#
#     }
#     es.index(index="users_index", id=id, body=elem)
#     id += 1



