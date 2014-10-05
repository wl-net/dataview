import paramiko

class SSH:
    def __init__(self):
        client = paramiko.SSHClient()

    def get_ssh_key(self, file=None):
        key = ""
        if file = None:
            key = ""
        else: 
            key = ""
        return paramiko.RSAKey(data=base64.decodestring(key))
    
    def _connect(self, hostname, username, ssh_key):
        pass

    def connect(self, hostname):
        pass

    def disconnect(self):
        client.close()

    def exec_command(self, command):
        return client.exec_command(command)

    def get_client(self):
        return client
