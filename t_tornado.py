import tornado.ioloop
from tornado import web, gen
from tornado.httpclient import AsyncHTTPClient


class MainHandler(web.RequestHandler):
    def get(self):
#        import pdb; pdb.set_trace()
        assert "GET" == self.request.method
        print 'request.args:', self.request.arguments

        op = self.get_argument('op', 'empty_op')    #?op=xxx
        self.write("op is: %s\n" %op)
        if 'stop' == op:
            tornado.ioloop.IOLoop.instance().stop()

class GenAsyncHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        url = self.get_argument('url')
        #curl http://localhost:8888/async/?url=http://www.bai.com
        #if not yield this, fetch_something() should not write() anything
        response = yield AsyncHTTPClient().fetch(url)    
        assert 200 == response.code
        self.write(response.body)
#        raise gen.Return(response.body)
#        self.render("template.html")

applicaiton = web.Application([
    (r"/", MainHandler),
    (r"/async/", GenAsyncHandler),
    ], 
    debug=True  #dynamic reload server after codes changed
)

def main():
    applicaiton.listen(8888)
    #from IPython import embed; embed()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
