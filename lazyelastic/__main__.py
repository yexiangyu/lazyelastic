from lazyelastic import LazyModel, get_connection
import uuid

# 在定义任何模型前，请必须进行初始化es的connection，这里的connection是singleton模式
get_connection(es_nodes=["test.internal.maimenggroup.com:9200"])

# 定义一个基础模型


class GenericEvent(LazyModel):
    _index = 'generic_event'  # es的index
    _cols = {  # 定义mapping，key和各自的类型生成函数
        "id": int,
        "name": str,
        "uuid": lambda: str(uuid.uuid4())
    }


# 继承GenericEvent，子类的_cols 属性，会和父类的_cols做一次合并
class AuthserverLog(GenericEvent):
    _index = 'authserver_log'
    _cols = {"timetag": int}


if __name__ == "__main__":
    s = AuthserverLog(id=1, name="john")
    g = GenericEvent()
    print(s)
    print(g)
    s.save()
    ret = AuthserverLog.search()
    for r in ret:
        print(r)
