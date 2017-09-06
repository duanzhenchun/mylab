#!/usr/bin/env python
# encoding: utf-8

import web

urls = (
    '/(.*)', 'index',
    '/(\d+)/node_stats', 'node_stats',
    '/sync', "sync",
    '/node_cut', "node_cut",
    '/users/list/(.+)', "list_users",
    )

render = web.template.render('templates/')

class node_stats:
    def GET(self, day):
        return day

class sync:
    def GET(self):
        return 'sync'

class list_users:
    def GET(self, name):
        return "Listing info about user: {0}".format(name)

class index:
    def GET(self, name):
        #  return 'root'
        return render.index(name)

app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()

