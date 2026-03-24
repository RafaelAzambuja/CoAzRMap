def normalize_snmp_string(value : str) -> str:
        """

        """
        if not value:
            return ""

        return value.strip('"')