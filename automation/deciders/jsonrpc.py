from automation.deciders import AbstractDecider
from dataview.transports.jsonrpc import JSONRPCClient


class JSONRPCDecider(AbstractDecider):
      
    def decide(self):
        """
        calls the remote JSON-RPC server to determine the outcome
        """
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'])

        ## TODO: call server and compare result