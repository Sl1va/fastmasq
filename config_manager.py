import json


class ConfigManager:
    def __init__(self, hosts: str, jsdb: str):
        self.hosts = hosts
        self.jsdb = jsdb

    def set_record(self, domain: str, addr: str):
        records = self.read_records()
        records[domain] = addr
        self.write_records(records)

    def get_record(self, domain: str):
        records = self.read_records()
        if domain in records:
            return records[domain]
        return None

    def delete_record(self, domain: str):
        records = self.read_records()
        if domain in records:
            del records[domain]
            self.write_records(records)
        else:
            print(f"{domain} is not in records table")

    def read_records(self):
        try:
            with open(self.jsdb, "r", encoding="utf-8") as jsstore:
                return json.load(jsstore)
        except:
            return {}

    def write_records(self, records: dict[str, str]):
        try:
            with open(self.jsdb, "w", encoding="utf-8") as jstore:
                json.dump(records, jstore, indent=4)
        except Exception as e:
            print(f"Failed to write records to json: {e}")
            return

        try:
            with open(self.hosts, "w", encoding="utf-8") as hostsfile:
                for domain, host in records.items():
                    print(f"{host:<16} {domain}", file=hostsfile)
        except Exception as e:
            print(f"Failed to write hosts: {e}")
