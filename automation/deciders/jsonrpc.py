from dataview.transports.JSONRPC import JSONRPCClient
from automation.deciders import AbstractDecider
class JSONRPCDecider(AbstractDecider):
    def __init__(self, conditons, configuration):
        super().__init__()
      
    def decide():
        """
        calls the remote JSON-RPC server to determine the outcome
        """
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'])
        
        
        
        