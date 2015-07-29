from tornado import gen, web, ioloop
import tcelery, tasks

tcelery.setup_nonblocking_producer()

class AsyncHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        tasks.echo.apply_async(args=['Hello world!'], callback=self.on_result)

    def on_result(self, response):
        self.write(str(response.result))
        self.finish()

class GenAsyncHandler(web.RequestHandler):
    @web.asynchronous
    @gen.coroutine
    def get(self):
        response = yield gen.Task(tasks.sleep.apply_async, args=[3])
        self.write(str(response.result))
        self.finish()

"""
#start server
python -m tcelery --port=8888 --app=tasks --address=0.0.0.0

#call
curl -X POST -d '{"args":["hello"]}' http://localhost:8888/apply-async/tasks.echo/
curl -X POST -d '{"args":[3]}' http://localhost:8888/apply-async/tasks.sleep/

#get result
curl http://localhost:8888/tasks/result/71ab097d-f083-414e-810b-983e7a4e59c1/
"""
