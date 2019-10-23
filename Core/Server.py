import logging
import logging.handlers
import os

from quarry.net.server import ServerFactory
from quarry.types.registry import LookupRegistry

from Core.Player import Player
from Core.Config import Config
from Core.PluginManager import PluginManager
from Core.CommandManager import CommandManager

levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


class Server(ServerFactory):
    protocol = Player

    def __init__(self):
        super(Server, self).__init__()

        self.config = Config()

        self.log_level = levels[self.config.get("server.log_level", "info")]
        self.motd = self.config.get("server.motd", "PyMine Server")
        self.online_mode = self.config.get("server.online_mode", True)
        self.max_players = self.config.get("server.max_players", 10)

        self.logger = logging.getLogger("Server")
        self.logger.setLevel(self.log_level)
        file = os.path.join(os.path.dirname(__file__), "..", "Logs", "server.log")
        filehandler = logging.handlers.RotatingFileHandler(file, maxBytes=10000, backupCount=1)
        filehandler.setLevel(self.logger.level)
        filehandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s : %(message)s"))

        self.logger.addHandler(filehandler)
        self.logger.info("Server started.")

        self.command_manager = CommandManager(self)
        self.plugin_manager = PluginManager(self, self.config.get("plugins", []))
        self.plugin_manager.call("start", self)

        self.registry = LookupRegistry.from_json(os.path.join(os.path.dirname(__file__), "Datas"))
