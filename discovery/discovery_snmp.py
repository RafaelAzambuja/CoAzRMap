from core.file_handler import ConfigFile
from subprocess import run

class SNMPMgmt:
    """
    """

    def __init__(self, snmp_agent_interface: str, cfg_file: ConfigFile):
        """
        """

        self.agent_interface = snmp_agent_interface
        self.cfg_file = cfg_file
        self.get_command = None
        self.getnext_command = None
        self.walk_command = None


    def connect(self) -> bool:
        '''

        '''
        timeout = str(self.cfg_file.read_cfg_file("snmp", "timeout", fallback="3"))
        retries = str(self.cfg_file.read_cfg_file("snmp", "retries", fallback="1"))
        
        # SNMPv3
        if self.cfg_file.read_cfg_file("snmpv3", "use_v3").lower() == "true":

            sec_level = str(self.cfg_file.read_cfg_file("snmpv3", "security_level"))
            snmp_user = str(self.cfg_file.read_cfg_file("snmpv3", "user"))
            auth_opt = str(self.cfg_file.read_cfg_file("snmpv3", "auth_option"))
            auth_pass = str(self.cfg_file.read_cfg_file("snmpv3", "auth_password"))
            priv_opt = str(self.cfg_file.read_cfg_file("snmpv3", "priv_option"))
            priv_pass = str(self.cfg_file.read_cfg_file("snmpv3", "priv_password"))

            base_cmd = ["snmpget",
                        "v3",
                        "-r", retries,
                        "-t", timeout,
                        "-l", sec_level,
                        "-u", snmp_user,
                        "-a", auth_opt,
                        "-A", auth_pass,
                        "-x", priv_opt,
                        "-X", priv_pass,
                        self.agent_interface
                    ]

            output = run(base_cmd + ["1.3.6.1.2.1.1.2.0"], capture_output=True, text=True, timeout = 5)

            if self.validate_snmp(output.stdout, output.returncode):

                self.version = "v3"
                self.vendor_oid = output.stdout.split()[3]

                self._prepare_commands(base_cmd)

                return True

        # SNMPv2c
        elif self.cfg_file.read_cfg_file("snmpv2c", "use_v2c").lower() == "true":

            communities_raw = self.cfg_file.read_cfg_file("snmpv2c", "communities")
            communities = [c.strip() for c in communities_raw.split(",") if c.strip()]

            for community in communities:
                base_cmd = [
                    "snmpget",
                    "-v2c",
                    "-r", retries,
                    "-t", timeout,
                    "-c", community,
                    self.agent_interface
                ]

                output = run(base_cmd + ["1.3.6.1.2.1.1.2.0"], capture_output=True, text=True, timeout = 5)

                if self.validate_snmp(output.stdout, output.returncode):

                    self.version = "v2c"
                    self.vendor_oid = output.stdout.split()[3]

                    self._prepare_commands(base_cmd)

                    return True

        return False

    def validate_snmp(self, response: str, return_code: int) -> bool:

        invalid_snmp_strings = (
        "No Such Object",
        "No Such Instance",
        "Timeout"
    )

        if return_code != 0 or not response:
            return False

        return not any(err in response for err in invalid_snmp_strings)

    def _prepare_commands(self, base_cmd: list[str]):
        self.get_command = base_cmd.copy()

        self.getnext_command = base_cmd.copy()
        self.getnext_command[0] = "snmpgetnext"

        self.walk_command = base_cmd.copy()
        self.walk_command[0] = "snmpwalk"
        self.walk_command.insert(2, "-Cc")

    def snmpget(self, oid: str) -> tuple[str, str]:
        '''
        Perform SNMP GetRequest.

        Args:
            oid (str): Object Identifier.

        Returns:
            tuple[Optional[str], Optional[str]]:
                (value, value_type) if successful,
                (None, None) otherwise.

        Example output:
            iso.3.6.1.2.1.1.5.0 = STRING: "hostname"
        '''

        command = self.get_command + [oid]
        output = run(command, capture_output=True, text=True)
        
        #print(f"Command: {command} | SNMP Output: {output.stdout} | SNMP Error: {output.stderr}")

        if self.validate_snmp(output.stdout, output.returncode):
            output.stdout = output.stdout.rstrip()
            output.stdout = output.stdout.split()
            value = " ".join(output.stdout[3:])
            value_type = output.stdout[2][:-1]
            return value, value_type
        
        return None, None

    def snmpgetnext(self, oid: str) -> tuple[str, str]:
        '''
        Perform SNMP GetNextRequest.

        Args:
            oid (str): Object Identifier.

        Returns:
            tuple[Optional[str], Optional[str]]:
                (value, value_type) if successful,
                (None, None) otherwise.
        '''

        command = self.getnext_command + [oid]
        output = run(command, capture_output=True, text=True)

        if self.validate_snmp(output.stdout, output.returncode):
            stdout = output.stdout.rstrip()
            stdout = stdout.split()
            value = " ".join(stdout[3:])
            value_type = stdout[2][:-1]
            return value, value_type
        
        return None, None

    def snmpwalk(self, oid: str) -> list[str]:
        
        # Utilizar snmpbulkwalk?

        ''' Perform SNMP Walk.

        Args:
            oid (str): Root Object Identifier.

        Returns:
            Optional[list[str]]:
                List of response lines if successful,
                None otherwise.
        '''

        command = self.walk_command + [oid]
        output = run(command, capture_output=True, text=True)
        if self.validate_snmp(output.stdout, output.returncode):
            output_list = output.stdout.split('\n')
            output_list.pop(-1)
            return output_list
    
        # print(f"SNMP Error: {output.stdout}")
        return None