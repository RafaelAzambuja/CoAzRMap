import json
import csv
import tempfile
import os
from pathlib import Path
from configparser import ConfigParser, NoSectionError, NoOptionError

class ConfigFile:
    def __init__(self):
        self.config_file_path = Path(__file__).resolve().parent / "config.ini"

        if not self.config_file_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file_path}")

        self.config = ConfigParser()
        self.config.read(self.config_file_path)

    def read_cfg_file(self, section: str, key: str, fallback=None) -> str:
        try:
            return self.config.get(section, key)
        except NoSectionError:
            raise KeyError(f"Section '{section}' not found in config file")
        except NoOptionError:
            raise KeyError(f"Key '{key}' not found in section '{section}'")
        except ValueError as e:
            raise ValueError(f"Invalid value for '{key}' in section '{section}': {e}")

class CSVFile:
    def __init__(self, csv_file):
        self.csv_file_path = Path(__file__).resolve().parent / "output" / csv_file

    def _create_csv(self):
        self.csv_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_file_path.unlink(missing_ok=True)
        self.csv_file_path.touch()

    def _atomic_write(self, data):
        
        path = self.csv_file_path
        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
            newline=""
        ) as tmp:

            if not data:
                tmp_name = tmp.name
            else:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(tmp, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                tmp_name = tmp.name

        os.replace(tmp_name, path)

class JsonFile:
    def __init__(self, json_file):
        self.json_file_path = Path(__file__).resolve().parent / "output" / json_file

    def _load_data(self):
        path = self.json_file_path

        if path.exists() and path.stat().st_size > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _create_json(self):
        self.json_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.json_file_path.unlink(missing_ok=True)
        self.json_file_path.touch()

    def _atomic_write(self, data):
        path = self.json_file_path
        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False
        ) as tmp:
            json.dump(data, tmp, indent=4)
            tmp_name = tmp.name

        os.replace(tmp_name, path)

    def add_to_category(self, category, item):
        """
        item can be a dict or a list of dicts
        """
        data = self._load_data()

        data.setdefault(category, [])

        if isinstance(item, list):
            data[category].extend(item)
        else:
            data[category].append(item)

        self._atomic_write(data)

    def save_all(self, data: dict):
        """
        Overwrite entire JSON file with provided data.
        """
        self._atomic_write(data)

    # def append_data(self, data):
    #     with open(self.json_file_path, 'w') as f:
    #         json.dump(data, f, indent=2)
