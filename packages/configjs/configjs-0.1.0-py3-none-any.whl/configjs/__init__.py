import json
from collections import namedtuple


class Config:
    def __init__(self, filename="config.json"):
        # Load the configuration from the specified JSON file
        with open(filename, "r") as file:
            config_data = json.load(file)

        # Convert the JSON data into a nested named tuple for easy attribute access
        self._config = self._json_object_hook(config_data)

    def _json_object_hook(self, d):
        # Convert a JSON object into a named tuple recursively
        return namedtuple("Config", d.keys())(
            *[
                self._json_object_hook(v) if isinstance(v, dict) else v
                for v in d.values()
            ]
        )

    def __getattr__(self, name):
        # Allow attribute access using the package name itself
        return getattr(self._config, name)


# Example usage:
if __name__ == "__main__":
    # Assuming the "config.json" file has the structure mentioned in the README
    config = Config()

    # Access configuration settings using the package name as attributes
    db_host = config.database.host
    db_port = config.database.port
    db_username = config.database.username
    db_password = config.database.password
    api_key = config.api_key

    # Print the configuration settings
    print(f"Database Host: {db_host}")
    print(f"Database Port: {db_port}")
    print(f"Database Username: {db_username}")
    print(f"Database Password: {db_password}")
    print(f"API Key: {api_key}")
