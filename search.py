from elasticsearch import Elasticsearch
import json
es = Elasticsearch()


class Searcher:
    def __init__(self) -> None:
        self.es = Elasticsearch()

    def search(self, key, method):
        ''' 搜索，返回一个由字典组成的列表结果。
        若没有满足条件返回None。
        method可以为 "id", "identifier", "date", "keywords", "year", "author", "abstract","title", "paper_id", "journal", "publisher"。
        当选取前一行个时返回的是论文，选取后1行个时返回的是作者'''
        searchQuery = {
            'query': {
                'match': {
                    method: key
                }
            }
        }

        if method in [
            "id", "identifier", "date", "keywords", "year", "author", "abstract","title", "paper_id", "journal", "publisher" ]:
            result = self.es.search(index="papers_index", body=searchQuery)
            return result['hits']['hits']
        elif method in ["userId","userName"]:
            result = self.es.search(index='users_index', body=searchQuery)
            return result['hits']['hits']
        else:
            print('No match result!')
            return None

if __name__ == '__main__':
    se = Searcher()
    result = se.search('Novelance', 'userName')
    print(json.dumps(result[0], indent=2, separators=(',', ';')))
# json格式化显示函数
