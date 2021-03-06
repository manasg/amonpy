import zmq
from amonpy.config import config

class ZeroMQHandler():
    def __init__(self, socktype=zmq.DEALER):
        self.ctx = zmq.Context.instance()
        self.socket = zmq.Socket(self.ctx, socktype)
        self.socket.setsockopt(zmq.LINGER, 100)
        # As there is no high water mark set - we don't really need this
        # Additionally, its not possible to set location of these yet
        # https://zeromq.jira.com/browse/LIBZMQ-410
        #self.socket.setsockopt(zmq.SWAP, 25000000) # 25MB disk swap
        
        address = "tcp://{0}".format(config.address)
        self.socket.connect(address)

    def close(self):
        self.socket.close()

    def post(self, data, type=None):
        data = {"type": type, "content" : data}
        if config.secret_key:
            data['secret_key'] = config.secret_key
        
        self.socket.send_json(data, zmq.NOBLOCK)

zeromq_handler = ZeroMQHandler()

