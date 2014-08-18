# coding=utf-8

SUBSCRIBE_MOVIE = '订阅电影'
CUR_MOVIES = 'current_movies.html'

Movie_type = 6 #mkv, 7:720p
Movie_thold = 7

Tos=['whille@163.com','meng3r@qq.com']

ME = 'english.onion.op'
PASSWORD = 'OP_english'

douban_token = '26813bd953cdac9e'
src_url = 'http://oabt.org/?cid=%d'
API_KEY = '09e7e2ad76917ac81db7a80863b47058'
API_SECRET = '42764a7149130882'
redirect_uri = 'http://54.250.166.126/spam/auth'
SCOPE = 'douban_basic_common,movie_basic_r'

 
Movie_head = """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
<style type="text/css">
.clearfix{display:block}
.subject{float:left;}
#mainpic{margin:3px 0 0 0;float:left;text-align:center;margin:3px 12px 0 0;max-width:155px;overflow:hidden}
</style>
</head>
<body>
"""
  
MOVIE_FMT = """
<div class="subject clearfix">
<div id="mainpic">
<a href="%s" target="_blank"><img src="%s" width="150px"></a>
</div>
<div>
<p>score: %s</p>
<p>title: %s</p>
<p>original_title: %s</p>
<p>year: %s</p>
<a href="%s">%s</a>
</div>
</div>
"""
 
