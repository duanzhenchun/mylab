# coding=utf-8
import re

g_noncsdiv = u'[^\u4e00-\u9fa5]+'
g_nonendiv = u'[^\w]+'
mostused = set(u'的一了是在人不有中')
#matching a url is complex, just to simplify here
SPECIAL_PATTERN = re.compile(ur'(#.+?#|\[.+?\]|https?:\/\/[.\/\w$&_-]+|@[0-9a-zA-Z\u4e00-\u9fa5_-]+)')


UPLOAD_LIMIT = 10 ** 9
MAX_RATIO = 1e4

