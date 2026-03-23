from utils.file_handler import ConfigFile

class SSHMgmt():
    def __init__(self, ssh_server_interface: str | None = None,
                 ssh_username: str | None = None,
                 ssh_password: str | None = None):
        self.cmd = []
        pass
    
    def test_ssh_on_host(host: str, ssh_port, ssh_username, ssh_password):
        pass

    def poll_ssh_active_hosts(hosts: list[str], cfg_file: ConfigFile) -> dict:
        pass