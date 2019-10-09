import logging
import os

from quarry.net.server import ServerFactory
from quarry.types.registry import LookupRegistry

from Core.Protocol import Protocol


class Factory(ServerFactory):
    protocol = Protocol
    motd = "PyMine Server"
    online_mode = True
    max_players = 10

    def __init__(self):
        super(Factory, self).__init__()

        self.logger = logging.getLogger("Server")
        self.logger.setLevel(self.log_level)
        self.logger.info("Server started.")

        self.registry = LookupRegistry.from_json(os.path.join(os.path.dirname(__file__), "Datas"))

