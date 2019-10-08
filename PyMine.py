from Core import Factory
from twisted.internet import reactor

factory = Factory()
factory.listen("127.0.0.1", 25565)
reactor.run()
