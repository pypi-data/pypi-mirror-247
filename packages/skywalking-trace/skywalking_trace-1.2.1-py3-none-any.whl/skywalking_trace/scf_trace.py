from skywalking.trace.context import get_context
from skywalking import Layer, Component
from skywalking.trace.tags import TagHttpMethod, TagHttpStatusCode, TagHttpParams
from skywalking.trace.carrier import Carrier
import json
import time

def Fg_trace(func):
    def wrapper(event, context):  
        if check_is_ckafka(event):
            return ckafka_wrapper(func,event, context)
        else:
            return http_wrapper(func,event, context)
    return wrapper
    
# 判断是否是数组
def is_array(object):
    if isinstance(object, list):
        return True
    else:
        return False

#判断是否为ckafka触发器数据    
def check_is_ckafka(event):
    records = event.get("Records")
    if records is not None and is_array(records):
        for item in records:
            ckafka = item.get('Ckafka')
            if ckafka is not None:
                return True
    return False

#api触发器
def http_wrapper(func,event, context):
    print("api触发器")
    try:
        carrier = Carrier()
        headers = event.get('headers')
        for item in carrier:
            if item.key.capitalize() == 'Sw8':
                item.val = headers.get('sw8')
            if item.key.capitalize() == 'Sw8-correlation':
                item.val = headers.get('sw8-correlation')
            if item.key.capitalize() in headers:
                item.val = headers.get(item.key.capitalize())
        path = event.get('path')
        params = event.get('body','')   
        httpMethod = event.get('httpMethod','')   
        resp = None
        with get_context().new_entry_span(op=path or '/', carrier=carrier, inherit=Component.General) as span:
            span.layer = Layer.Http
            span.component = Component.Flask
            span.tag(TagHttpMethod(httpMethod))    
            span.tag(TagHttpParams(params))
            resp = func(event, context)
            # statusCode = resp.get("statusCode")
            # if statusCode is not None and statusCode >= 400:
            #     span.error_occurred = True
            # span.tag(TagHttpStatusCode(statusCode))
            print("执行fg_trace装饰器成功")
        time.sleep(2)
        return resp
    except Exception as e:
        print(f"执行fg_trace装饰器失败: {e}")
        return func(event, context)


#ckafka触发器
def ckafka_wrapper(func,event, context):
    print("ckafka触发器")
    try:
        headers = json.loads(event.get('Records')[0].get('Ckafka').get('msgBody')).get('headers')
        topic = event.get('Records')[0].get('Ckafka').get('topic')  
        print('Ckafka:'+topic)
        resp = None
        with get_context().new_entry_span(
                    op=f"Kafka/{topic}/Consumer/"  or '') as span:
            carrier = Carrier()
            for item in carrier:
                if item.key.capitalize() == 'Sw8':
                    item.val = headers.get('sw8')
                    #print(item.key.capitalize()+"=="+headers.get('sw8'))
                if item.key.capitalize() == 'Sw8-correlation':
                    item.val = headers.get('sw8-correlation')
                    #print(item.key.capitalize()+"=="+headers.get('sw8-correlation'))
                if item.key.capitalize() in headers:
                    item.val = headers.get(item.key.capitalize())
                    #print(item.key.capitalize()+"=="+headers.get(item.key.capitalize()))
            span.extract(carrier)
            span.layer = Layer.MQ
            span.component = Component.KafkaConsumer
            resp = func(event, context)
            print("执行fg_trace装饰器成功")
        time.sleep(2)
        return resp
    except Exception as e:
        print(f"执行fg_trace装饰器失败: {e}")
        return func(event, context)