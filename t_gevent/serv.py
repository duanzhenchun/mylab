#ref http://www.coder4.com/archives/1522

from SocketServer import ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from SocketServer import TCPServer

TCPServer.request_queue_size = 10000

#Logic function
def add(a, b):
    return a + b

#Logic function 2
def gen(n):
    return '0' * n

#create server
server = SimpleXMLRPCServer(('', 8080), SimpleXMLRPCRequestHandler,False)
server.register_function(add, "add")
server.register_function(gen, "gen")
server.serve_forever()
