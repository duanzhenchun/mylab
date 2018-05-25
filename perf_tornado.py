#!/usr/bin/env python

# ab -c 100 -n 10000 http://localhost:6060/

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("Hello, world")
        self.finish()


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    port = sys.argv[1]
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
