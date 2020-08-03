import logging
import logging.handlers
import os

from quarry.net.server import ServerFactory

from core.Protocol import Protocol
from core.utils import Config
from core.PluginManager import PluginManager
from core.CommandManager import CommandManager

levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


class Server(ServerFactory):
    protocol = Protocol

    def __init__(self):
        super(Server, self).__init__()

        self.config = Config()

        self.log_level = levels[self.config.get("server.log_level", "info")]
        self.motd = self.config.get("server.motd", "PyMine Server")
        self.online_mode = self.config.get("server.online_mode", True)
        self.max_players = self.config.get("server.max_players", 10)

        self.logger = logging.getLogger("Server")
        self.logger.setLevel(self.log_level)
        file = os.path.join(os.path.dirname(__file__), "..", "logs", "server.log")
        filehandler = logging.handlers.RotatingFileHandler(file, maxBytes=10000, backupCount=1)
        filehandler.setLevel(self.logger.level)
        filehandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s : %(message)s"))

        self.logger.addHandler(filehandler)
        self.logger.info("Server started on {}:{}.".format(self.config.get("server.ip", "127.0.0.2"), self.config.get("server.port", 25565)))

        self.command_manager = CommandManager(self)
        self.plugin_manager = PluginManager(self, self.config.get("plugins", []))
        self.plugin_manager.call("start", self)
