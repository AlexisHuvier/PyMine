import json
import os
import importlib


class Plugin:
    def __init__(self, file):
        self.path = os.path.join(os.path.dirname(__file__), "..", "Plugins", os.path.dirname(file))
        with open(os.path.join(self.path, os.path.basename(file)), "r") as f:
            data = json.load(f)
        self.file = file
        self.name = data["name"]
        self.description = data["description"]
        self.module = importlib.import_module("Plugins."+os.path.dirname(file)+"."+data["main_file"])
        self.instance = self.module.instance


class PluginManager:
    def __init__(self, factory, plugins):
        self.factory = factory
        self.plugins = [Plugin(i) for i in plugins]
        self.call("start", self.factory)

    def call(self, function, *args):
        for i in self.plugins:
            fnc = getattr(i.instance, function)
            if fnc:
                fnc(*args)

