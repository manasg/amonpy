import time
import amonpy
import logging
import zmq
import urllib2
import json

runs = 10000
http_address = 'http://127.0.0.1:2464'

amonpy.config.address = '127.0.0.1:5464'
amonpy.config.protocol = 'zeromq'

start = time.time()
for i in range(0, runs):
    amonpy.log({"key": "value"})

print "ZeroMQ - {0}".format(time.time()-start) 

amonpy.config.address = http_address
amonpy.config.protocol = 'http'

start = time.time()
for i in range(0, runs):
    amonpy.log({"key": "value"})

print "HTTP - {0}".format(time.time()-start) 

logger = logging.getLogger('amonpy_application')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('bench.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

start = time.time()
for i in range(0, runs):
    _dict = {"key": "value"}
    logger.info(str(_dict))

print "Standard logging - {0}".format(time.time()-start) 

def post_zeromq():
    address = "tcp://127.0.0.1:5464"
    data = {"type": 'test', "content" : 'test'}
    context = zmq.Context.instance()
    
    socket = context.socket(zmq.DEALER)
    socket.connect(address)
    socket.send_json(data, zmq.NOBLOCK)
    context.destroy()
    
start = time.time()
for i in range(0, runs):
    post_zeromq()

print "ZeroMQ Raw - {0}".format(time.time()-start) 

    
start = time.time()
for i in range(0, runs):
    data = {'message': 'test me', 'tags':['debug','test']}
    json_string = json.dumps(data)

    req = urllib2.Request("{0}/api/log".format(http_address)",
                      headers = {"Content-Type": "application/json"},
                      data = json_string)
    f = urllib2.urlopen(req)

print "HTTP Raw - {0}".format(time.time()-start) 

