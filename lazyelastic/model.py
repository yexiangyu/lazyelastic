import json
import time
from lazyelastic.connections import get_connection
import logging

LOG = logging.getLogger("lazyelastic")


class LazyDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, key))

    def __setattr__(self, key, value):
        if key in self._fields:
            self[key] = self.__fields[key](value)
        else:
            raise AttributeError(r"'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, key))


class LazyModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["_conn"] = get_connection()
        _cols = attrs.get('_cols', None)
        if _cols is not None:
            for base in [b for b in bases if hasattr(b, '_cols')]:
                __cols = base._cols
                __cols.update(_cols)
                _cols = __cols
            attrs['_cols'] = _cols
        return type.__new__(cls, name, bases, attrs)


class LazyModel(LazyDict, metaclass=LazyModelMetaclass):
    _index = None
    _cols = {}
    _conn = None

    def __init__(self, **kw):
        _kw = {}
        for k, vt in self._cols.items():
            v = kw.get(k, None)
            _kw[k] = vt(v) if v is not None else vt()
        if self.__class__.__name__ != 'LazyModel' and not self._index:
            raise ValueError("index not available in model %s" %
                             (repr(type(self))))
        super().__init__(**_kw)

    def save(self):
        start = time.time()
        ret = self._conn.es.index(self._index, body=json.dumps(self))
        LOG.info("save %s, delta=%f", self, time.time() - start)

    async def async_save(self):
        start = time.time()
        ret = await self._conn.aes.index(self._index, body=json.dumps(self))
        LOG.info("save %s, delta=%f", self, time.time() - start)
        return ret

    @classmethod
    def search(cls, **kw):
        start = time.time()
        query = {'query': {'match_all': kw}} if kw else {}

        ret = cls._conn.es.search(
            index=cls._index,
            body=query,
        )
        LOG.info("search return %d result, delta=%f",
                 ret["hits"]["total"]["value"],
                 time.time() - start)
        ret = [cls(**hit['_source']) for hit in ret["hits"]["hits"]]
        return ret

    @classmethod
    async def async_search(cls, **kw):
        start = time.time()
        query = {'query': {'match_all': kw}} if kw else {}

        ret = await cls._conn.aes.search(
            index=cls._index,
            body=query,
        )
        LOG.info("search return %d result, delta=%f",
                 ret["hits"]["total"]["value"],
                 time.time() - start)
        ret = [cls(**hit['_source']) for hit in ret["hits"]["hits"]]
        return ret
