#!/usr/bin/env python
# encoding: utf-8

import web
import json

urls = (
    '/', 'index',
    '/post', 'post'
)


class index:
    def GET(self):
        return "Hello, world!"


class post:
    def POST(self):
        data = json.loads(web.data())
        return "Hello %s!" % data.get("name", "")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
