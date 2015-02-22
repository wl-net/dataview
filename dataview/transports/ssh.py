import paramiko

class SSH:
    def __init__(self):
        self.client = paramiko.SSHClient()

    def get_ssh_key(self, file=None):
        key = ""
        if file is None:
            key = ""
        else: 
            key = ""
        return paramiko.RSAKey(data=base64.decodestring(key))
    
    def _connect(self, username, hostname, port, ssh_key):
        self.client.connect(hostname, port, username)
        pass

    def connect(self, username, hostname, port=22):

        self._connect(username, hostname, port, key)
        pass

    def disconnect(self):
        self.client.close()

    def exec_command(self, command):
        return self.client.exec_command(command)

    def get_client(self):
        return self.client