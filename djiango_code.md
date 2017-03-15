#django 相关代码

##1、原始sql操作

    class SQLQuery(object):
        """
        操作原始sql，操作模拟list
        """
        def __init__(self,sql="",using='trade'):
            from django.db import connections
            self.__dbs = connections[using]
            self.sql = sql
            self._cursor = self.__dbs.cursor()
            self._cursor.execute(self.sql)
            self.keyss = self.keys()
    
        def count(self):
            cus = self.__dbs.cursor()
            cus.execute('select count(1) from (%s)' % self.sql)
            count = cus.fetchall()[0][0]
            cus.close()
            return count
    
        def keys(self): return [r[0].lower() for r in self._cursor.description]
        def __dict(self,arge): 
            return dict(zip(self.keyss,map(self.__encoder,arge)))
    
        def __encoder(self,val):
            if isinstance(val,decimal.Decimal):
                return float(val)
            return val
    
        def __iter__(self):
            for r in self._cursor:
                yield dict(zip(self.keyss,map(self.__encoder,r)))
    
        def __getitem__(self,nm):
            nm += 1
            cus = self.__dbs.cursor()
            cus.execute('select * from (select rownum as resnm,res.* from (%s) res where rownum <= %d) where resnm = %d' % (self.sql,nm,nm))
            items = self.__dict(cus.fetchall()[0][1:])
            cus.close()
            return items
    
    
        def __getslice__(self,i=0,j=0):
            cus = self.__dbs.cursor()
            cus.execute('select * from (select rownum as resnm,res.* from (%s) res where rownum <= %d) where resnm >= %d' % (self.sql,j,i+1))
            items = [self.__dict(r[1:]) for r in cus.fetchall()]
            cus.close()
            return items
    
        def __len__(self): return self.count()
        def __del__(self): self._cursor.close()
        def __repr__(self): return '<Sql object[%s]>'%','.join(map(str,['<sqldict object>' for r in xrange(self.count())]))
        def __str__(self): return '<Sql object[%s]>'%','.join(map(str,['<sqldict object>' for r in xrange(self.count())]))