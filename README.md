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
<<<<<<< HEAD
           
           
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
=======
>>>>>>> 7a79badc60b0c52ee9b47e7149e90cf6b5792c05
