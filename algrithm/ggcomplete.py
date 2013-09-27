# -*- coding: utf-8 -*-

from sgmllib import SGMLParser
import urllib2
import urllib

# Define the class that will parse the suggestion XML
class PullSuggestions(SGMLParser):

   def reset(self):
      SGMLParser.reset(self)
      self.suggestions = []
      self.queries = []

   def start_suggestion(self, attrs):
      for a in attrs:
         if a[0] == 'data': self.suggestions.append(a[1])

   def start_num_queries(self, attrs):
      for a in attrs:
         if a[0] == 'int': self.queries.append(a[1])

def read_q(q):
    query = urllib.urlencode({'q' : q})
    url = "http://google.com/complete/search?output=toolbar&hl=zh-CN&%s" % query
    res = urllib2.urlopen(url)
    parser = PullSuggestions()
    parser.feed(res.read())
    parser.close()

    for i in parser.suggestions:
       print i.decode('gbk')
   
if __name__ == '__main__':
    import sys
    if len(sys.argv) >1:
        q= sys.argv[1]
    else:
        q='mengge'
    read_q(q)
