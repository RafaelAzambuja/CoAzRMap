#import paramiko

class SSHMgmt:
    def __init__(self, ssh_server_interface: str | None = None,
                 ssh_username: str | None = None,
                 ssh_password: str | None = None):
        self.cmd = []
        pass