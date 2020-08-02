import json
import os


class Config:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "config.json"), "r") as f:
            self.config = json.load(f)

    def get(self, key, default):
        keys = key.split(".")
        if len(keys) == 1:
            return self.config.get(key, default)
        else:
            value = self.config
            for i in keys:
                if i != keys[-1]:
                    value = value[i]
                else:
                    value = value.get(i, default)
            return value
