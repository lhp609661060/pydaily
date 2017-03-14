#python 日常

##1、简易线程
启动一个不相关的任务，并且不需要关心结果。
    
    import threading
    
    def thread_fn(f):
    
        @wraps(f)
        def _fn(*a, **b):
            t = threading.Thread(target=f, args=a, kwargs=b)
            t.start()
            
        return _fn
        
##2、本地缓存
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
        
##3、redis缓存
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