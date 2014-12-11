from SocketServer import ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from gevent import monkey

#Threaded XML-RPC && Monkey Patch
monkey.patch_socket() #Just 2 line!
monkey.patch_thread() #Just 3 line!
monkey.patch_select() #Just 3 line!
class TXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass

#Logic function
def add(a, b):
    return a + b

#Logic function 2
def gen(n):
    return "0" * n

#create server
server = TXMLRPCServer(('', 8080), SimpleXMLRPCRequestHandler)
server.register_function(add, "add")
server.register_function(gen, "gen")
server.serve_forever()
