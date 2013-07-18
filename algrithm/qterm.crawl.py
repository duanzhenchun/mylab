#!/usr/bin/env python 
# -*- coding: gbk -*- 
# 
# filename: astro_rss.py 
# Author: kangkang <kanger@gmail.com> 2006 
# Licence: GPLv2 
  
import qterm, sys 
import time 
  
lp = long(sys.argv[0]) 
  
import feedparser 
  
url = "http://www4.newsmth.net/rss.php?gAstrology" 
  
from datetime import date, timedelta 
tomorrow_s = date.today() + timedelta(days=1) 
tomorrow = tomorrow_s.strftime("%Y-%m-%d") 
  
def getData(): 
     feed = feedparser.parse(url) 
     all_data = [] 
     for item in feed["items"]: 
         data = [] 
         if item['title'].find(tomorrow) != -1: 
                 data.append(item['title'].encode("gbk")) 
                 # remove the post title and qmd, forgive me 
                 data.append("<br />".join(item['summary'].encode("gbk").split("<br /><br />")[1:]).split("<br />--<br />")[0].replace('<br />', '\n')) 
                 # orig message 
                 # data.append(.replace("<br />","\n")) 
                 all_data.append(data) 
     # reverse... 
     all_data.reverse() 
     return all_data 
  
# main 
for data in getData(): 
     # post data 
     qterm.sendParsedString(lp, "^p") 
     # title 
     qterm.sendParsedString(lp, data[0]) 
     qterm.sendParsedString(lp, "\n\n") 
     # content 
     qterm.sendParsedString(lp, data[1]) 
     qterm.sendParsedString(lp, "\n来源：水木社区(BBSBot (at) newsmth.net)") 
     qterm.sendParsedString(lp, "^wf^M") 
     time.sleep(.2) 
  
# jump to the last line 
qterm.sendParsedString(lp, "$") 
