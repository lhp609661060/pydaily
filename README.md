# python 日常

## 1、简易线程
启动一个不相关的任务，并且不需要关心结果。
    
    import threading
    
    def thread_fn(f):
    
        @wraps(f)
        def _fn(*a, **b):
            t = threading.Thread(target=f, args=a, kwargs=b)
            t.start()
            
        return _fn
        
## 2、本地缓存
把数据存储到本地内存中，可以用于加载一些常用全局变量

    def cache_func(f, *a, **b):
        """
        缓存数据，缓存10分钟
        """
        f.cache = {}
        f._time = time.time()
    
        def _fn(*_a,**_b):
    
            if _b:
                k = _a, frozenset(b.items())
            else:
                k = _a
    
            _cache = f.cache
    
            if (time.time() - f._time) > 10 * 60:
                _cache[k] = f(*_a,**_b)
                
            if k not in _cache:
                _cache[k] = f(*_a,**_b)
    
            return _cache[k]
    
        return _fn
        
## 3、redis缓存
简易缓存数据

    def cache_as(time_out=None):
        def _fn(callback, *arg, **kwarg):
            def _callback(*arg, **kwarg):
                cache_key = 'key_{0}_{1}_{2}_{3}'.format(callback.__module__, callback.__name__, arg, kwarg)
                data = cache.get(cache_key)
                if data:
                    return data
    
                data = callback(*arg, **kwarg)
                if isinstance(time_out, int):
                    cache.set(cache_key, data, time_out)
                else:
                    cache.set(cache_key, data)
                return data
    
            if hasattr(callback, '__name__'):
                _callback.__name__ = callback.__name__
            if hasattr(callback, '__dict__'):
                _callback.__dict__ = callback.__dict__
            if hasattr(callback, '__doc__'):
                _callback.__doc__ = callback.__doc__
    
            return _callback
    
        return _fn
        
## 4、性能测试函数

    
    import time

    def timer(func):
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            print func.__name__, t2 - t1
            return result
    
        return wrapper

    class Timer:
        def __init__(self, name=None):
            self._name = name
    
        def __enter__(self):
            self._start = time.time()
    
        def __exit__(self, exc_type, exc_val, exc_tb):
            self._end = time.time()
            
    >>>@timer
       def test():
           print 123
           
    >>>with Timer('name'):
           code ...
           
           
## excel 读取
解析excel数据toJson

    class ExcelSheet(object):

        def __init__(self, sheet):
            self.sheet = sheet
            self.__datas = []
    
        def get_title(self):
            return []
    
        def start_row(self):
            return 1
    
        def __row_is_empty(self, datas):
            emptys = (None, '')
            for v in datas:
                if v not in emptys:
                    return True
            return False
    
        @property
        def sheet_datas(self):
            if self.__datas:
                return self.__datas
    
            self.__datas = [x for x in self.iter_sheet_datas]
            return self.__datas
    
        def get_unicode(self,value):
            if isinstance(value, (unicode, str)):
                return value.strip().replace('\n', '')
            if isinstance(value, float) and value % 1 == 0:
                value = int(value)
                return value
            return value
    
        @property
        def iter_sheet_datas(self):
            title = self.get_title()
            for i in xrange(self.start_row(), self.sheet.nrows):
                row_data = [self.get_unicode(v) for v in self.sheet.row_values(i)]
                if not self.__row_is_empty(row_data): continue
                yield dict(zip(title, row_data))

                
           
## 类型强制转换
方便进行数据运算

    import base64
    import datetime
    import json
    
    class CT(object):
        """
        强制类型转换工具
        """
    
        def __init__(self,val=None):
            self.val = val
    
        def __float__(self):
            if not self.val: return 0.0
            return self.__to_type(float,self.val,0.0)
    
        def __trunc__(self):
            if not self.val: return 0
            return self.__to_type(int,self.val,0)
    
        def __int__(self):
            if not self.val: return 0
            return self.__to_type(int,self.val,0)
    
        def __str__(self):
            if not self.val: return ''
            return self.__to_type(str,self.val,'')
    
        def __to_type(self,fn,val,default=None):
            try: 
                return fn(val)
            except Exception, e: 
                return default
    
        def toString(self):
            return unicode(self.val)
    
        def toJson(self, fn):
            return json.loads(self.val)
    
        def toJsonString(self):
            pass
    
        def toDate(self):
            pass
    
        def toInt(self):
            pass
    
        def toFloat(self):
            pass
    
        def toBool(self):
            pass
    
        def toBate(self):
            pass
    
        def toBase64(self):
            pass


## 惰性应用
应当于一个对象的惰性加载

    class Lazy(object):
        __data = {}
    
        def __init__(self, obj):
            self.__obj = obj
    
    
        def __getattr__(self, name):
            fn = getattr(self.__obj, name)
            if hasattr(fn, '__call__'):
                def _f(*a, **b):
                    key = (name, a, tuple(b.items()))
                    if key in self.__data:
                        return self.__data[key]
    
                    r = fn(*a, **b)
                    self.__data[key] = r
                    return self.__data[key]
    
                return _f
            
    >>> class Test(object):
            
            def hello(self):
                print 'hello'
                return 0
                
    >>> t = Lazy(Test())
    >>> t.hello()
    hello
    0
    >>> t.hello()
    0
    >>> t.hello()
    0
    
    
## requests 使用代理抓取数据
通过代理ip来完成"千锋教育"优惠页面ip收集任务

    # conding=utf-8

    import requests 
    from selenium import webdriver
    import time
    
    class Ip(object):
        def __init__(self):
            for ip in self.ips():
                try:
                    self.open_d(ip)
                except Exception as e:
                    print e
    
    
        def ips(self):
            r = requests.get('http://api.zdaye.com/?api=201704131532443528&rtype=1&ct=200').text.split('\n')
            return [_.replace('\r', '') for _ in r]
    
        def open_d(self, ip):
            print ip, '='*30
            browser=webdriver.PhantomJS()
    
            proxy=webdriver.Proxy()
            proxy.http_proxy=ip
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            browser.set_page_load_timeout(20)
            browser.get('http://www.mobiletrain.org/jiip/?url_code=K1XCb1WN')
            browser.find_element_by_xpath('//a[@class="btn2"]').click()
            time.sleep(10)
            browser.close()
            
## pandas 简单使用
使用pandas 比对数据差异

    import pandas as pd
    
    mytable = pd.read_excel('mytable.xls') # 读取本地数据
    jrtable = pd.read_excel('jrtable.xls') # 读取验证数据
    
    mytable_dd = mytable[mytable[u'产品名称']==u'订单融资'] #挑出自己的数据 相当与filter
    jrtable_dd = jrtable[jrtable[u'产品名称']==u'订单融资'] #挑出目标数据 相当与filter
    
    aa = mytable_dd[[u'金融订单号','amount']].groupby(u'金融订单号').sum() #去重 =groupby
    bb = jrtable_dd[[u'融资订单号',u'融资放款额']].groupby(u'融资订单号').sum() #去重 =groupby
    
    aa.to_dict()
    bb.to_dict()
    