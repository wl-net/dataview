class JSONRPC:
    def __init__(self):
        pass

    def connect(self, target, apikey, certificate, port=22)
        pass

    def disconnect(self):
        self.client.close()

    def call(self, command):
        return self.client.exec_command(command)

    def get_client(self):
        return self.client
