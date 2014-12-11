import time

class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type=None):
        print instance, type
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res

class C(object):
    @cached_property
    def now(self):
        return time.time()

c=C()
for i in range(3):
    print c.now
