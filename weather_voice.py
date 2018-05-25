# -*- coding: utf-8 -*-
# @Time     : 2017/1/15 15:16
# @Author   : woodenrobot

import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
    '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
    'i/537.36',
}

num_dict = {
    1: u'一',
    2: u'二',
    3: u'三',
    4: u'四',
    5: u'五',
    6: u'六',
    7: u'七',
    8: u'八',
    9: u'九',
    0: u'零'
}


def numtozh(num):
    num = int(num)
    if 100 <= num < 1000:
        b_num = num // 100
        s_num = (num - b_num * 100) // 10
        g_num = (num - b_num * 100) % 10
        if g_num == 0 and s_num == 0:
            num = u'%s百' % (num_dict[b_num])
        elif s_num == 0:
            num = u'%s百%s%s' % (num_dict[b_num], num_dict.get(s_num, ''),
                                num_dict.get(g_num, ''))
        elif g_num == 0:
            num = u'%s百%s十' % (num_dict[b_num], num_dict.get(s_num, ''))
        else:
            num = u'%s百%s十%s' % (num_dict[b_num], num_dict.get(s_num, ''),
                                 num_dict.get(g_num, ''))
    elif 10 <= num < 100:
        s_num = num // 10
        g_num = (num - s_num * 10) % 10
        if g_num == 0:
            g_num = ''
        num = u'%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    elif 0 <= num < 10:
        g_num = num
        num = u'%s' % (num_dict[g_num])
    elif -10 < num < 0:
        g_num = -num
        num = u'零下%s' % (num_dict[g_num])
    elif -100 < num <= -10:
        num = -num
        s_num = num // 10
        g_num = (num - s_num * 10) % 10
        if g_num == 0:
            g_num = ''
        num = u'零下%s十%s' % (num_dict[s_num], num_dict.get(g_num, ''))
    return num


def get_weather():
    # 下载墨迹天气主页源码
    res = requests.get('http://tianqi.moji.com/', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find(
        'div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    temp = numtozh(int(temp))
    weather = soup.find(
        'div', attrs={'class': 'wea_weather clearfix'}).b.getText()
    sd = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()
    sd_num = re.search(r'\d+', sd).group()
    sd_num_zh = numtozh(int(sd_num))
    sd = sd.replace(sd_num, sd_num_zh)
    wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()
    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    aqi_num = re.search(r'\d+', aqi).group()
    aqi_num_zh = numtozh(int(aqi_num))
    aqi = aqi.replace(aqi_num, aqi_num_zh).replace(' ', u',空气质量')
    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()
    sd = sd.replace(' ', u'百分之').replace('%', '')
    aqi = 'aqi' + aqi
    info = info.replace(u'，', ',')
    # 获取今天的日期
    today = datetime.now().date().strftime('%Y年%m月%d日').decode('utf8')
    # 将获取的信息拼接成一句话
    text = u'早上好！今天是%s,天气%s,温度%s摄氏度,%s,%s,%s,%s' % \
           (today, weather, temp, sd, wind, aqi, info)
    return text


def text2voice(text):
    url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
          'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
    # 直接播放语音
    url = url.encode('utf8')
    print 'mplayer "%s"' %url
    os.system('mplayer "%s"' %url)


def main():
    # 获取需要转换语音的文字
    text = get_weather()
    print text
    # 获取音乐文件绝对地址
    # mp3path2 = os.path.join(os.path.dirname(__file__), u'2.mp3')
    # 先播放一首音乐做闹钟
    # os.system('mplayer %s' % mp3path2)
    # 播报语音天气
    text2voice(text)


if __name__ == '__main__':
    main()
