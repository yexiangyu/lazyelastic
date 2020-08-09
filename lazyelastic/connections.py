from elasticsearch import (
    AsyncElasticsearch,
    Elasticsearch
)

__instance = None


class __ElasticSearch(object):
    def __init__(self, es_nodes=["localhost:9200"], es_username=None, es_password=None):
        self.aes = AsyncElasticsearch(
            es_nodes,
            http_auth=(es_username, es_password)
        )
        self.es = Elasticsearch(
            es_nodes,
            http_auth=(es_username, es_password)
        )


def _get_connection(**kw):
    global __instance
    __instance = __ElasticSearch(**kw)


def get_connection(**kw):
    global __instance
    if not kw:
        return __instance
    if __instance is None:
        _get_connection(**kw)
    return __instance
