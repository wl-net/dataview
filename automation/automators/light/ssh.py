from dataview.transports.ssh import SSH

class LightSSHAutomator:
    def __init__(self, user, hostname, light_id):
        self.user = user
        self.hostname = hostname
        self.light_id = light_id
        
    def turn_on(self):
        ssh = SSH()
        ssh.connect(self.hostname)
        ssh.exec_command('dvc light-on %s' % self.light_id)
        
    def turn_off(self):
        ssh = SSH()
        ssh.connect(self.hostname)
        ssh.exec_command('dvc light-off %s' % self.light_id)

    def set_brightness(self, brightness):
        ssh = SSH()
        ssh.connect(self.hostname)
        ssh.exec_command('dvc light-brightness %s %s' % (self.light_id, brightness))
