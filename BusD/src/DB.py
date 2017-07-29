import redis
import ast
from util import *


class Rdscli(object):
    def __init__(self):
        self.cli = redis.client.Redis()
        self.route = 'bus'
        self.busuid = 'busuid'

    def routename(num, direct, type):
        return ':'.join(map(str, (self.route, num, direct, type)))

    def set(self, uid, busnum, direct, loc , type='need'):
        return self.cli.hset(self.routename(busnum, direct, type), uid, loc)

    def getall(self, busnum, direct, type='need'):
        res = self.cli.hgetall(self.routename(busnum, direct, type))
        return ast.literal_eval(res)

    def remove(self, uid, busnum, direct, loc, type='need'):
        return self.cli.hdel(self.routename(busnum, direct, type), uid)

    def new_uid(self):
        return self.cli.incr(self.busuid)


Cli = Rdscli()

if __name__ == '__main__':
    pass
