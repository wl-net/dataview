import requests
import json

class JSONRPCClient:
    def __init__(self):
        self.request_id = 1
        pass

    def connect(self, target, apikey, certificate=None):
        self.target = target
        self.apikey = apikey
        self.certificate = certificate
        pass

    def disconnect(self):
        self.client.close()

    def call(self, command, arguments):
        req = {"jsonrpc": "2.0", "method": command, "params": arguments, "id": self.request_id}
        self.request_id +=1
        r = requests.post(self.target, data = json.dumps(req),
                          headers = { 'Authorization', 'Token: ' + self.apikey },
                          verify=self.certificate)

        if r.status_code == 200:
            return r.json()['result']
        raise Exception(r.status_code)

    def get_client(self):
        return self.client
