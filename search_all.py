from elasticsearch import Elasticsearch
import json
es = Elasticsearch()

class Searcher_all:
    def __init__(self) -> None:
        self.es = Elasticsearch()
    def search(self, key, method):
        ''' 搜索，返回一个由字典组成的列表结果。
        若没有满足条件返回None。
        method可以为 "id", "identifier", "date", "keywords", "year", "author", "abstract","title", "paper_id", "journal", "publisher"。
        当选取前一行个时返回的是论文，选取后1行个时返回的是作者'''
        str_split = key.split()
        L =[]
        for t in str_split:
            print(t)
            searchQuery = {
                'query': {
                    'match': {
                        method: t
                    }
                }
            }
            wildcard_query = {
                "query": {
                    "wildcard": {
                        method: {
                            "value": "*t*"

                        }
                    }
                }
            }

            if method in [
                "arXiv_ID", "title", "author", "abstract", "Link", "Published", "pdfPath", "Categories"]:
                result = self.es.search(index='index',body=searchQuery)['hits']['hits']
                result_wild = self.es.search(index='index',body=wildcard_query)['hits']['hits']
                L.append(result)
                # print(result)
                L.append(result_wild)
                # print(result_wild)
            else:
                print('No match result!')
                return None
        llist = []
        list = []
        result = L
        for j in result:
            for i in j:
                # print("i")
                # print(i)
                if i["_source"]["title"] in llist:
                    continue
                else:
                    list.append(i)
                    llist.append(i["_source"]["title"])

        return list
#
# if __name__ == '__main__':
#     llist=[]
#     list =[]
#     se = Searcher()
#     result = se.search("geo A", 'title')
#     for j in result:
#         for i in j:
#             print("i")
#             print(i)
#             if i["_source"]["title"] in llist:
#                 continue
#             else:
#                 list.append(i)
#                 llist.append(i["_source"]["title"])
#                 print(json.dumps(i, indent=2, separators=(',', ';')))