from Core import Server
from twisted.internet import reactor

factory = Server()
factory.listen("127.0.0.1", 25565)
reactor.run()
