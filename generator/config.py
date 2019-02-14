import os.path
import sys

import pkg_resources
import yaml


class Config:
    config_paths = ["./github-changelog-generator.yaml", "~/.config/github-changelog-generator.yaml"]

    def __init__(self):
        try:
            with open(self.get_config_path(), 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    self.api_token = config["api_token"]  # type:str
                    self.labels_to_ignore = set(config["labels_to_ignore"])
                    self.sort_by_labels = config["sort_by_labels"]  # type:list
                    self.repositories = config["repositories"]  # type:list
                    self.is_matomo = config["is_matomo"]  # type:bool
                    if self.is_matomo:
                        self.compare_config()
                except KeyError as e:
                    sys.exit("required option '{}' is missing from the config".format(e.args[0]))
        except ValueError:
            self.api_token = "none_found"

    def get_config_path(self) -> str:
        for path in self.config_paths:
            if os.path.isfile(path):
                return path
        raise ValueError()

    def compare_config(self) -> None:
        used_config = self.__dict__
        default_config_file = pkg_resources.resource_filename('generator', 'defaultconfig.yaml')

        with open(default_config_file, 'r') as stream:
            default_config = yaml.safe_load(stream)
            default_config["labels_to_ignore"] = set(default_config["labels_to_ignore"])

            for key, value in default_config.items():
                if key in ["api_token"]:
                    continue
                elif key not in used_config:
                    print("Key {} is missing from user config".format(key))
                elif value != used_config[key]:
                    print("{} differs from recommended config".format(key))
                    print("default config:")
                    print(value)
                    print("own config:")
                    print(used_config[key])


config = Config()
