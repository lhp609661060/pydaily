#python 日常#

#1、简易线程#
启动一个不相关的任务，并且不需要关心结果。
    
    import threading
    
    def thread_fn(f):
    
        @wraps(f)
        def _fn(*a, **b):
            t = threading.Thread(target=f, args=a, kwargs=b)
            t.start()
            
        return _fn