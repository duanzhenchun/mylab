#!/usr/bin/env python

from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
from pycallgraph import GlobbingFilter

config = Config(max_depth=40)
config.trace_filter = GlobbingFilter(
    exclude=[
    'pycallgraph.*',
    'json.*',
    'httplib.*',
#    'socket.*',
    'mimetools.*',
    'rfc822.*',
    'logging.*',
#    'multiprocessing.*',
    'calendar.*',
    'ctypes.*',
])

graphviz = GraphvizOutput(output_file='t_callgraph.png')

def t_chunck():
    from test_chunked import test_upload, test_download, txt2test
    txt=txt2test()
    test_upload(txt)
    res = test_download()
    assert txt ==  res

def t_start():
    from run import start_test
    start_test()

def t_tornado():
    import sys
    sys.path.append('../')
    import t_tornado
    t_tornado.main()

with PyCallGraph(output=graphviz, config=config):
#    t_start()
#    t_chunck()
    t_tornado()

"""
#run
python tests/tcgraph.py 
feh test_chunked.png 

pycallgraph --max-depth 20 -e "pycallgraph.*" -e "rfc822.*" -e "numbers.*"  -e "calendar.*" -e "Cookie.*" -e "multiprocessing.*" -e "logging.*" -e "platform" -e "urllib.*" -e "ctypes.*"  -e "httplib.*" -e "socket.*"  -e "json.*" -e "urllib2.*" -e "pickle.*" graphviz --output-file=out.png tests/test_chunked.py


"""
