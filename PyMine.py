from core import Server
from twisted.internet import reactor

factory = Server()
factory.listen(factory.config.get("server.ip", "127.0.0.1"), factory.config.get("server.port", 25565))
reactor.run()
