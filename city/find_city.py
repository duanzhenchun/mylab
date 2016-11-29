#!/usr/bin/env python
# encoding: utf-8

dic = {}

def init():
    with open("./city.csv") as f:
        for line in f:
            lst = line.strip().split()
            Id, name, pId, _, py, pinyin  = lst[:6]
            if pinyin in dic:
                print Id, name, pId, py, pinyin
            dic[pinyin] = (Id, pId, py, pinyin)


def api(city_pinyin):
    print dic[city_pinyin]

init()
