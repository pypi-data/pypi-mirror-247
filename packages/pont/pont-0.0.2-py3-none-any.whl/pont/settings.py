import logging
from pathlib import Path

import platformdirs
from strictyaml import Enum, Int, Map, Seq, Str, YAMLValidationError
from strictyaml import load as strictyaml_load


class SettingsError(Exception):
    pass


class ProxySettings:
    protocol: str
    remote_host: str
    remote_port: int
    local_port: int
    local_host: str


class Settings:
    # This is the schema for the pont.yml file validation
    PROXY_SCHEMA = Map(
        {
            "protocol": Enum(["http", "redis"]),
            "remote_host": Str(),
            "remote_port": Int(),
            "local_port": Int(),
            "local_host": Str(),
        }
    )
    SCHEMA = Map({"host": Str(), "port": Int(), "proxies": Seq(PROXY_SCHEMA)})

    port: int
    host: str
    proxies: list[ProxySettings]
    config_file: Path | None

    def __init__(self) -> None:
        self.host = "127.0.0.1"
        self.port = 8888
        self.proxies = []
        self.config_file = None

    def load(self):
        current_directory = Path.cwd()
        pont_yaml_path = current_directory / "pont.yml"
        if pont_yaml_path.exists():
            self.load_file(pont_yaml_path)
        else:
            pont_yaml_path = self.user_config_directory() / "pont.yml"
            if pont_yaml_path.exists():
                self.load_file(pont_yaml_path)
            else:
                logging.warning("No pont.yml file found, using default settings")

    def user_config_directory(self) -> Path:
        return Path(platformdirs.user_config_dir("pont"))

    def load_file(self, pont_yaml_path: Path):
        try:
            with pont_yaml_path.open("r") as file:
                pont_yaml = strictyaml_load(file.read(), schema=self.SCHEMA)
                self.port = int(pont_yaml["port"])
                self.host = str(pont_yaml["host"])
                for proxy in pont_yaml["proxies"]:
                    proxy_settings = ProxySettings()
                    proxy_settings.protocol = str(proxy["protocol"])
                    proxy_settings.remote_host = str(proxy["remote_host"])
                    proxy_settings.remote_port = int(proxy["remote_port"])
                    proxy_settings.local_port = int(proxy["local_port"])
                    proxy_settings.local_host = str(proxy["local_host"])
                    self.proxies.append(proxy_settings)
            self.config_file = pont_yaml_path
            logging.info(f"Settings loaded from {pont_yaml_path}")
        except (OSError, YAMLValidationError) as error:
            raise SettingsError(f"Error loading {pont_yaml_path}: {error}") from error


if __name__ == "__main__":
    # Use to test the code from the command line
    settings = Settings()
    settings.load()
    print(f"The port is {settings.port}")
    for proxy in settings.proxies:
        print(f"Proxy {proxy.protocol} listening on {proxy.local_port}")
