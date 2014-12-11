class Singleton(object):
    _instance = None

    def __new__(self, *a,**kw):
        print '__new__, before __init__'
        if not self._instance:
            print super(Singleton, self)
            self._instance = super(Singleton, self).__new__(self, *a, **kw)
        return self._instance

    def __init__(self, *a, **kw):
        print '__init__'
        self.lst=range(10)


    def __del__(self):
        print '__del__'

    def __call__(self, *a, **kw):
        print '__call__'

    def __str__(self):
        return "I'm Singleton"

    def __cmp__(src, dst):
        src.a-dst.a

    def __getitem__(self, i):
        return self.lst[i]

    def __getslice(self, i,j):
        return self.lst[i:j]

"""
    def __len__(self):
        print '__len__'
"""

def test():
    a = Singleton()
    b = Singleton()
    assert id(a) == id(b)
    print a()
    print a
    print a[2]
    print a[2:5]
    del a


test()

