# coding=utf-8

import json
import re
from utils import *

Tweet_table='Weibo_tweet'


Basic_tweet_fields="""
id,0
text
created_at:CREATE_TIME
source
truncated,0
in_reply_to_status_id:REPLY_STATUS_ID,0
in_reply_to_user_id:REPLY_USER_ID,0
in_reply_to_screen_name:REPLY_SCREEN_NAME
thumbnail_pic
bmiddle_pic
original_pic
"""

More_tweet_fields = """
reposts_count:RT_COUNT,0
comments_count:CT_COUNT,0
attitudes_count:FAVORITE,0
"""

User_fields="""
id:USER_ID,0
screen_name
created_at:USER_CREATE_TIME
province
city
location
description
url
profile_image_url:IMAGE_URL
domain
gender
followers_count:FOLLOWS_COUNT,0
friends_count:FRIENDS_COUNT,0
statuses_count:STATUS_COUNT,0
verified_type:VERIFIED
"""

Sina_type=1
RT_pre='RT_'


Gender_map={'m':1,'f':2,'n':0}
def map_gender(s):
    return Gender_map.get(s)

"""
0:未认证，对应Verify_type<0
1:个人认证，对应verify_type=0
2:未知，对应不到上面的各种类型
3:企业认证，对应verify_type>=1，且不包含达人认证
4:达人认证,对应verify_type>=200 && verify_type<=300
"""
def map_verified(vtype):
    if vtype<0:
        return 0
    elif vtype==0:
        return 1
    elif 0<vtype<200:
        return 3
    elif 200<vtype<300:
        return 4
    else:
        return 2


def init_field(s, prefix=''):
    dic = {}
    for l in s.split('\n'):
        l=l.strip()
        if not l:
            continue
        default=''
        if ',' in l:
            l,default=l.split(',')
        if ":" in l:
            origin, field = l.split(':')
        else:
            origin, field = l, l.upper()
        dic[origin]=(prefix+field, default)
    return dic
User_field_dic=init_field(User_fields)
RT_User_field_dic=init_field(User_fields, RT_pre)

Tweet_field_dic=init_field(Basic_tweet_fields)
Tweet_more_field= init_field(More_tweet_fields)

def get_normal_text(text):
    # 格式化字符串，去掉4字节的utf-8编码字符
    text_repr = repr(text)
    if text_repr.find('\\U000') != -1:
        text = re.sub('(\\\\U000\w+)', '', text_repr)
        text = eval(text)
        return text
    else:
        return text

Map_userfn={'created_at': fmt_create_at, 'verified_type': map_verified, 
    'gender':map_gender, 'description':get_normal_text}
       

def get_user(user, field_dic=User_field_dic):
    dic={}
    for k,(v,default) in field_dic.iteritems():
        dic[v] = user.get(k, default)
        if default and not dic[v]:
            dic[v] = default
    for k, fn in Map_userfn.iteritems():
        dic[field_dic[k][0]]=fn(dic[field_dic[k][0]])
    return dic


def get_tweet(tweet):
    dic={}
    for k, (v,default) in Tweet_field_dic.iteritems():
        dic[v] = tweet.get(k, default)
        if default and not dic[v]:
            dic[v] = default
    for k, (v,default) in Tweet_more_field.iteritems():
        dic[v] = tweet.get(k, default)
        if default and not dic[v]:
            dic[v] = default

    dic['TYPE']= Sina_type
    dic['SOURCE_URL'], dic['SOURCE'] = get_source_url(dic['SOURCE'])
    dic['SOURCE']=get_normal_text(dic['SOURCE'])
    dic['TEXT']=get_normal_text(dic['TEXT'])
    user = tweet.get('user')
    dic.update(get_user(user))
    origin_tweet = tweet.get('retweeted_status')
    dic['CREATE_TIME']= fmt_create_at(dic['CREATE_TIME'])
    if origin_tweet:
        for k, (v,default) in Tweet_field_dic.iteritems():
            v=RT_pre+v
            dic[v] = origin_tweet.get(k, default)
            if default and not dic[v]:
                dic[v] = default
        dic[RT_pre+'SOURCE_URL'], dic[RT_pre+'SOURCE'] = get_source_url(dic[RT_pre+'SOURCE'])
        dic[RT_pre+'CREATE_TIME']=fmt_create_at(dic[RT_pre+'CREATE_TIME'])
        dic[RT_pre+'TEXT']=get_normal_text(dic[RT_pre+'TEXT'])
        dic[RT_pre+'SOURCE']=get_normal_text(dic[RT_pre+'SOURCE'])
        rt_user = origin_tweet.get('user')
        dic.update(get_user(rt_user, RT_User_field_dic))
    return dic


PAT_URL = re.compile('<\S*a href="([^"]*)" .*?>(.*?)<')
def get_source_url(s):
    url, source = '',''
    res = PAT_URL.search(s)
    if res:
        url,source=res.groups()
#    else:
#        print 'source_url not found:', s
    return url, source

#tweet=json.load(open('../../data/weibotext.json','r'))

