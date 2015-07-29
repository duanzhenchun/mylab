#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types


def gen(arg):
    print 'gen_start'
    got = yield arg
    print 'got:', got
    yield got


def call():
    f = gen(1)
    assert isinstance(f, types.GeneratorType)
    assert True

    try:
        f.next()
        for i in range(2, 8):
            res = f.send(2)
            print res
    except (StopIteration) as e:
        print 'exception', e, res
