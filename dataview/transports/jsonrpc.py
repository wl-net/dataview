from dataview.models import X509Certificate
from django.core.exceptions import ObjectDoesNotExist

import requests
import json


class JSONRPCClient(object):
    def __init__(self):
        self.request_id = 1

    def connect(self, target, apikey, certificate=None):
        self.target = target
        self.apikey = apikey
        self.certificate = certificate

    def disconnect(self):
        pass # this transport does not stay open

    def call(self, command, arguments):
        req = {"jsonrpc": "2.0", "method": command, "params": arguments, "id": self.request_id}
        self.request_id += 1

        if self.certificate:
            try:
                cert_file = X509Certificate.get_file_from_str(self.certificate)
            except (ObjectDoesNotExist, FileNotFoundError):
                cert_file = X509Certificate.create_from_str(self.certificate).get_location()

            r = requests.post(self.target, data=json.dumps(req),
                              headers={'Authorization': 'Token ' + self.apikey},
                              verify=cert_file)
        else:
            r = requests.post(self.target, data=json.dumps(req),
                              headers={'Authorization': 'Token: ' + self.apikey})

        if r.status_code == 200:
            return r.json()['result']

        raise Exception(r.status_code)

    def get_client(self):
        return self.client

    def healthcheck(self):
        pass